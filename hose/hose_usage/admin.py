from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    HoseAssociation,
    HoseContent,
    HoseUser
)
from .forms import CustomUserCreationForm, CustomUserChangeForm


class HoseAssociationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hose_name']}),
    ]


class CustomerUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = HoseUser
    list_display = ['email', 'username',]


admin.site.register(HoseAssociation, HoseAssociationAdmin)
admin.site.register(HoseContent)
admin.site.register(HoseUser, CustomerUserAdmin)
