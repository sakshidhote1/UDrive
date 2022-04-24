from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(tblcontactus)
admin.site.register(tblcustomersignup)


admin.site.site_header  =  "UDrive"
admin.site.site_title  =  "UDrive admin site"
admin.site.index_title  =  "UDrive Admin"