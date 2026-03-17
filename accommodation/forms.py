from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, CheckInRecord, CheckOutRequest


# ---------------- USER REGISTER ----------------

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


# ---------------- PROFILE FORMS ----------------

class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["student_id"]


class AdminProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["admin_department"]


# ---------------- CHECK-IN FORM ----------------

class CheckInRecordForm(forms.ModelForm):

    class Meta:
        model = CheckInRecord
        fields = ["student", "room_number"]


    def clean(self):
        cleaned_data = super().clean()

        student = cleaned_data.get("student")
        room_number = cleaned_data.get("room_number")

        errors = []

        # check if student has active check-in
        if student:
            if CheckInRecord.objects.filter(student=student, status="active").exists():
                errors.append("This student already has an active check-in.")

        # check if room is occupied
        if room_number:
            if CheckInRecord.objects.filter(room_number=room_number, status="active").exists():
                errors.append("This room already has an active check-in.")

        if errors:
            raise forms.ValidationError(
                ["Cannot create check-in record. Possible reasons:"] + errors
            )

        return cleaned_data


# ---------------- CHECK-OUT REQUEST ----------------

class CheckOutRequestForm(forms.ModelForm):

    class Meta:
        model = CheckOutRequest

        fields = [
            "requested_check_out_date",
            "reason",
            "issues",
            "comments"
        ]

        widgets = {
            "requested_check_out_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "reason": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "issues": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
            "comments": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }


# ---------------- ADMIN REVIEW CHECK-OUT ----------------

class CheckOutStatusForm(forms.ModelForm):

    class Meta:
        model = CheckOutRequest
        fields = ["status", "admin_note"]

        widgets = {
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
            "admin_note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            })
        }