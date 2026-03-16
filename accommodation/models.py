from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# ---------------- USER PROFILE ----------------

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    student_id = models.CharField(max_length=20, blank=True, null=True)

    admin_department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# ---------------- CHECK-IN RECORD ----------------

class CheckInRecord(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('checked_out', 'Checked Out'),
    )

    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    room_number = models.CharField(max_length=10)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    check_in_date = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - Room {self.room_number}"


# ---------------- CHECK-OUT REQUEST ----------------

class CheckOutRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    check_in_record = models.ForeignKey(
        CheckInRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    room_number = models.CharField(max_length=10, null=True, blank=True)

    requested_check_out_date = models.DateField()

    reason = models.CharField(max_length=100)

    issues = models.TextField(blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    admin_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.get_status_display()}"


# ---------------- ROOM INSPECTION ----------------

class RoomInspection(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('fixing', 'Fixing'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # ⭐ 新增房间号
    room_number = models.CharField(max_length=10, null=True, blank=True)

    issues = models.TextField(blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - Room {self.room_number}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role="student")