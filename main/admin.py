from django.contrib import admin
from .models import Client, RequestType, ClientRequest
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.admin import AdminSite
from .decorators import staff_member_required_403

class CustomAdminSite(AdminSite):
    # Overrides the admin_view method to customize permission checks and caching behavior
    def admin_view(self, view, cacheable=False):
        # Wraps the original admin view with your custom staff_member_required_403 decorator
        # This ensures:
        # - Only authenticated staff users can access the admin views
        # - Unauthenticated users get redirected to login
        # - Authenticated non-staff users get HTTP 403 Forbidden instead of redirect
        view = staff_member_required_403(view)
        # If the view should not be cached, wraps it with Django's never_cache decorator
        # to prevent browsers and proxies from caching sensitive admin pages
        if not cacheable:
            from django.views.decorators.cache import never_cache
            view = never_cache(view)
        # Returns the wrapped view, now protected by your custom access control
        return view
# Instantiate your custom admin site, so you can register your models with it    
custom_admin_site = CustomAdminSite(name='custom_admin')

# Inline editing for ClientRequest within Client table(model) admin
class ClientRequestInline(admin.TabularInline):
    model = ClientRequest
    extra = 1
    fields = ('request_type', 'status', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True
       

# Register Client table(model) with custom admin options
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact_number', 'company_url', 'created_at', 'is_active')
    search_fields = ('name', 'email', 'contact_number', 'company_url')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact_number', 'company_url', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

custom_admin_site.register(Client, ClientAdmin)

# Register Request Type table(model)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('id', 'name')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )
custom_admin_site.register(RequestType, RequestTypeAdmin)

# Register Client Request Type table(model)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'request_type', 'status', 'description','created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__name', 'request_type__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('client', 'request_type', 'status')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        updated_count = queryset.update(status='Completed')
        self.message_user(request, f'{updated_count} requests marked as completed.')
    mark_as_completed.short_description = 'Mark selected requests as completed'
custom_admin_site.register(ClientRequest, ClientRequestAdmin)

class UsersAdmin(DefaultUserAdmin):
    # Inherit Django's built-in UserAdmin to get all user admin features.
    # You can override list_display or other attributes if desired.
    pass
custom_admin_site.register(User, UsersAdmin)
