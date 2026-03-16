from django.contrib import admin
from .models import UserProfile, CheckInRecord, CheckOutRequest

admin.site.register(UserProfile)
admin.site.register(CheckInRecord)
admin.site.register(CheckOutRequest)
# Register your models here.
