from django.contrib import admin

from pester.models import *

class APIAdmin(admin.ModelAdmin):
    list_display = ['name', 'key']

class CarrierAdmin(admin.ModelAdmin):
    list_display = ['name', 'gateway']
    ordering = ['name']

class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone_number']
    ordering = ['last_name']

class RecipientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone_number']
    ordering = ['last_name']

class PatternAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'code']

class PesteringAdmin(admin.ModelAdmin):
    pass

class ImageDataAdmin(admin.ModelAdmin):
    list_display = ['search_term', 'url', 'adult_safety_level']

class PesteringManagerRunAdmin(admin.ModelAdmin):
    list_display = ['run_time', 'completed']
    ordering = ['-run_time']

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class PesteringAttemptAdmin(admin.ModelAdmin):
    list_display = ['attempt_time',
                    'success',
                    'pestering',
                    'image',
                    'pestering_manager_run']
    ordering = ['-attempt_time']
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class PesteringExceptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_delelte_permission(self, request, obj=None):
        return False

admin.site.register(API, APIAdmin)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Pestering, PesteringAdmin)
admin.site.register(ImageData, ImageDataAdmin)
admin.site.register(PesteringManagerRun, PesteringManagerRunAdmin)
admin.site.register(PesteringAttempt, PesteringAttemptAdmin)
admin.site.register(PesteringException, PesteringExceptionAdmin)
