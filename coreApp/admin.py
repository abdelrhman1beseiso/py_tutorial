from django.contrib import admin

from coreApp.models import Topic, UserProgress , Chapter

# Register your models here.
admin.site.site_header = "Core App Admin"
admin.register([Chapter, Topic, UserProgress])  # Register your models here