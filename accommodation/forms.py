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

        widgets = {
            "student": forms.Select(attrs={
                "class": "form-control"
            }),

            "room_number": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


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
            "requested_check_out_date": forms.DateInput(attrs={"type": "date"})
        }


# ---------------- ADMIN REVIEW CHECK-OUT ----------------

class CheckOutStatusForm(forms.ModelForm):

    class Meta:
        model = CheckOutRequest
        fields = ["status", "admin_note"]