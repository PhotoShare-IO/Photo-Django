from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "get_full_name",
    )
    search_fields = ("email", "first_name", "surname")
