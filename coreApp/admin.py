from django.contrib import admin

from coreApp.models import Topic , Chapter

# Register your models here.
admin.site.site_header = "Core App Admin"
admin.register([Chapter, Topic])  # Register your models here