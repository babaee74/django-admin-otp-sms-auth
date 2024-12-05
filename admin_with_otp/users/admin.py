from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import  UserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from custom_admin.sites import admin_site


class UserAdminConfig(UserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    search_fields = ('mobile',)
    ordering = ('mobile',)
    list_display = ('mobile', 'is_active', 'is_staff',)
    list_display_links = ("mobile",)

    fieldsets = (
        (None, {'fields':('mobile',)}),
        ('Permissions',{'fields':('is_staff', 'is_active',)}),
        ('Password', {'fields': ('password',)})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ('mobile','password1', 'password2', )}
        ),
    )
    


# Now register the new UserAdmin...
# admin.site.register(CustomUser, UserAdminConfig)
admin_site.register(CustomUser, UserAdminConfig) #! custom admin instance
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
