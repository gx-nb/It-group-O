from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import UserProfile, CheckInRecord, CheckOutRequest, RoomInspection
from .forms import (
    UserRegistrationForm,
    CheckInRecordForm,
    CheckOutRequestForm,
    CheckOutStatusForm
)


# ---------------- LOGIN ----------------

def login_view(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        else:
            error = "Invalid username or password"

    return render(request, "accommodation/login.html", {"error": error})


# ---------------- REGISTER ----------------

def register_view(request):

    if request.method == "POST":

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Registration successful")

            return redirect("login")

    else:
        form = UserRegistrationForm()

    return render(request, "accommodation/register.html", {"form": form})


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


# ---------------- DASHBOARD ----------------

@login_required
def dashboard_view(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    context = {"profile": profile}

    # ---------------- STUDENT ----------------
    if profile.role == "student":

        check_in = CheckInRecord.objects.filter(
            student=profile,
            status="active"
        ).first()

        check_out_requests = CheckOutRequest.objects.filter(
            student=profile
        ).order_by("-created_at")

        inspections = RoomInspection.objects.filter(
            student=profile
        ).order_by("-created_at")

        # -------- Allow Create Checkout Logic --------
        allow_create_checkout = True

        for req in check_out_requests:
            if req.status in ["pending", "approved", "completed"]:
                allow_create_checkout = False
                break

        context["check_in"] = check_in
        context["check_out_requests"] = check_out_requests
        context["inspections"] = inspections
        context["allow_create_checkout"] = allow_create_checkout


    # ---------------- ADMIN ----------------
    elif profile.role == "admin":

        check_in_records = CheckInRecord.objects.all().order_by("-check_in_date")
        check_out_requests = CheckOutRequest.objects.all().order_by("-created_at")
        inspections = RoomInspection.objects.all().order_by("-created_at")

        # -------- Inspection Search --------
        search = request.GET.get("search")

        if search:
            inspections = inspections.filter(
                Q(student__user__username__icontains=search) |
                Q(room_number__icontains=search) |
                Q(issues__icontains=search)
            )

        # -------- Check-out Search --------
        checkout_search = request.GET.get("checkout_search")

        if checkout_search:
            check_out_requests = check_out_requests.filter(
                Q(student__user__username__icontains=checkout_search) |
                Q(room_number__icontains=checkout_search)
            )

        # -------- Check-in Search --------
        checkin_search = request.GET.get("checkin_search")

        if checkin_search:
            check_in_records = check_in_records.filter(
                Q(student__user__username__icontains=checkin_search) |
                Q(room_number__icontains=checkin_search)
            )

        context["check_in_records"] = check_in_records
        context["check_out_requests"] = check_out_requests
        context["inspections"] = inspections

    return render(request, "accommodation/dashboard.html", context)


# ---------------- DELETE CHECK-IN (ADMIN) ----------------

@login_required
def delete_check_in(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    record = get_object_or_404(CheckInRecord, pk=pk)

    record.delete()

    return redirect("dashboard")


# ---------------- CREATE CHECK-IN ----------------

@login_required
def create_check_in_record(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    if request.method == "POST":

        form = CheckInRecordForm(request.POST)

        if form.is_valid():

            room_number = form.cleaned_data["room_number"]
            student = form.cleaned_data["student"]

            student_exists = CheckInRecord.objects.filter(
                student=student,
                status="active"
            ).exists()

            if student_exists:
                return redirect("create_check_in")

            room_exists = CheckInRecord.objects.filter(
                room_number=room_number,
                status="active"
            ).exists()

            if room_exists:
                return redirect("create_check_in")

            record = form.save(commit=False)

            record.check_in_date = timezone.now().date()
            record.status = "active"

            record.save()

            return redirect("dashboard")

    else:

        form = CheckInRecordForm()

    return render(request, "accommodation/create_check_in.html", {"form": form})


# ---------------- EDIT CHECK-IN ----------------

@login_required
def edit_check_in(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    record = get_object_or_404(CheckInRecord, pk=pk)

    if record.status == "checked_out":
        return redirect("dashboard")

    if request.method == "POST":

        form = CheckInRecordForm(request.POST, instance=record)

        if form.is_valid():

            room_number = form.cleaned_data["room_number"]

            room_exists = CheckInRecord.objects.filter(
                room_number=room_number,
                status="active"
            ).exclude(pk=record.pk).exists()

            if room_exists:
                return redirect("edit_check_in", pk=pk)

            form.save()

            return redirect("dashboard")

    else:

        form = CheckInRecordForm(instance=record)

    return render(
        request,
        "accommodation/create_check_in.html",
        {"form": form, "edit": True}
    )


# ---------------- CREATE CHECK-OUT REQUEST ----------------

@login_required
def create_check_out_request(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "student":
        return redirect("dashboard")

    check_in = CheckInRecord.objects.filter(
        student=profile,
        status="active"
    ).first()

    if not check_in:
        messages.warning(request, "You do not have an active check-in.")
        return redirect("dashboard")

    last_request = CheckOutRequest.objects.filter(
        student=profile
    ).order_by("-created_at").first()

    if last_request:

        if last_request.status == "pending":
            messages.warning(request, "You already have a pending checkout request.")
            return redirect("dashboard")

        elif last_request.status == "approved":
            messages.warning(request, "Your checkout request has already been approved.")
            return redirect("dashboard")

        elif last_request.status == "completed":
            messages.warning(request, "Your checkout has already been completed.")
            return redirect("dashboard")

    if request.method == "POST":

        form = CheckOutRequestForm(request.POST)

        if form.is_valid():

            checkout = form.save(commit=False)

            checkout.student = profile
            checkout.check_in_record = check_in
            checkout.room_number = check_in.room_number
            checkout.status = "pending"

            issues = request.POST.getlist("issues")
            checkout.issues = ", ".join(issues)

            checkout.save()

            messages.success(request, "Checkout request submitted successfully.")

            return redirect("dashboard")

    else:

        form = CheckOutRequestForm()

    return render(
        request,
        "accommodation/create_check_out.html",
        {"form": form, "room_number": check_in.room_number}
    )


# ---------------- REVIEW CHECK-OUT ----------------

@login_required
def review_check_out_request(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    checkout = get_object_or_404(CheckOutRequest, pk=pk)

    applications = CheckOutRequest.objects.filter(
        student=checkout.student
    ).order_by("-created_at")

    if request.method == "POST":

        form = CheckOutStatusForm(request.POST, instance=checkout)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:

        form = CheckOutStatusForm(instance=checkout)

    return render(
        request,
        "accommodation/review_check_out.html",
        {"form": form, "check_out": checkout, "applications": applications}
    )


# ---------------- INSPECTION ----------------

@login_required
def inspection(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    check_in = CheckInRecord.objects.filter(
        student=profile,
        status="active"
    ).first()

    if not check_in:
        messages.warning(request, "You do not have an active check-in.")
        return redirect("dashboard")

    room_number = check_in.room_number

    if request.method == "POST":

        condition = request.POST.get("condition")
        issues = request.POST.getlist("issues")
        comments = request.POST.get("comments")

        if condition == "no":

            RoomInspection.objects.create(
                student=profile,
                room_number=room_number,
                issues="No issues",
                comments="",
                status="completed"
            )

        else:

            RoomInspection.objects.create(
                student=profile,
                room_number=room_number,
                issues=", ".join(issues),
                comments=comments,
                status="submitted"
            )

        return redirect("dashboard")

    return render(request, "accommodation/inspection.html")


# ---------------- FIX INSPECTION ----------------

@login_required
def fix_inspection(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    inspection = get_object_or_404(RoomInspection, pk=pk)

    if inspection.status == "submitted":
        inspection.status = "fixing"
        inspection.save()

    return redirect("dashboard")


# ---------------- DELETE INSPECTION ----------------

@login_required
def delete_inspection(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    inspection = get_object_or_404(RoomInspection, pk=pk)

    if profile.role == "admin":
        inspection.delete()
        return redirect("dashboard")

    if inspection.student != profile:
        return redirect("dashboard")

    if inspection.status == "fixing":
        return redirect("dashboard")

    inspection.delete()

    return redirect("dashboard")


# ---------------- EDIT CHECK-OUT ----------------

@login_required
def edit_check_out(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    checkout = get_object_or_404(CheckOutRequest, pk=pk)

    if checkout.student != profile:
        return redirect("dashboard")

    if checkout.status != "pending":
        return redirect("dashboard")

    if request.method == "POST":

        form = CheckOutRequestForm(request.POST, instance=checkout)

        if form.is_valid():

            obj = form.save(commit=False)

            issues = request.POST.getlist("issues")
            obj.issues = ", ".join(issues)

            obj.save()

            return redirect("dashboard")

    else:

        form = CheckOutRequestForm(instance=checkout)

    return render(
        request,
        "accommodation/create_check_out.html",
        {"form": form, "room_number": checkout.room_number}
    )


# ---------------- DELETE CHECK-OUT ----------------

@login_required
def delete_check_out(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    checkout = get_object_or_404(CheckOutRequest, pk=pk)

    if checkout.student != profile:
        return redirect("dashboard")

    if checkout.status != "pending":
        return redirect("dashboard")

    checkout.delete()

    return redirect("dashboard")


# ---------------- FINAL CHECK-OUT ----------------

@login_required
def final_check_out(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    checkout = get_object_or_404(CheckOutRequest, pk=pk)

    record = checkout.check_in_record

    checkout.status = "completed"
    checkout.save()

    if record:
        record.status = "checked_out"
        record.save()

    return redirect("dashboard")


# ---------------- DELETE CHECKOUT (ADMIN) ----------------

@login_required
def delete_checkout_admin(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    checkout = get_object_or_404(CheckOutRequest, pk=pk)

    checkout.delete()

    return redirect("dashboard")


# ---------------- EDIT INSPECTION ----------------

@login_required
def edit_inspection(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    inspection = get_object_or_404(RoomInspection, pk=pk)

    if inspection.student != profile:
        return redirect("dashboard")

    if inspection.status == "fixing":
        return redirect("dashboard")

    if request.method == "POST":

        issues = request.POST.getlist("issues")
        comments = request.POST.get("comments")

        inspection.issues = ", ".join(issues)
        inspection.comments = comments

        inspection.save()

        return redirect("dashboard")

    return render(
        request,
        "accommodation/inspection.html",
        {"inspection": inspection}
    )
@login_required
def complete_inspection(request, pk):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "admin":
        return redirect("dashboard")

    inspection = get_object_or_404(RoomInspection, pk=pk)

    if inspection.status == "fixing":
        inspection.status = "completed"
        inspection.save()

    return redirect("dashboard")