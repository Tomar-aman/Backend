from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(OTPVerification)
admin.site.register(APICallLog)

# Register your models here.
