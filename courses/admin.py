from django.contrib import admin
from courses.models import Instructor


# Register your models here.
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "course", "affiliation", "created_at", "profile_image")
    list_filter = ("course", "code")
    search_fields = ("name", "code", "affiliation")
