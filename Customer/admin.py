from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomerProfile, StaffProfile,Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display=('customer','staff','token_number','is_active','in_queue','is_used')


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Staff Profile'
    fk_name = 'user'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

    def get_inlines(self, request, obj):
        """Dynamically return the appropriate inline based on role"""
        if obj is not None:
            if obj.role == 'customer':
                return [CustomerProfileInline]
            elif obj.role == 'staff':
                return [StaffProfileInline]
        return []


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image','ration_card_number', 'district', 'state',)
    search_fields = ('user__username', 'ration_card_number')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'center_assigned', 'district', 'state','noOfTokenBooked','tokenUsed')
    search_fields = ('user__username', 'staff_id', 'center_assigned')
