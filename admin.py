from django.contrib import admin
from pester.models import Carrier, User, Recipient, Pattern, Pestering, Image 
from pester.models import PesteringManagerRun, PesteringAttempt, PesteringException

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
    list_display = ['name', 'description']

class PesteringAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    pass

class PesteringManagerRunAdmin(admin.ModelAdmin):
    pass

class PesteringAttemptAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class PesteringExceptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Carrier, CarrierAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(Pestering, PesteringAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(PesteringManagerRun, PesteringManagerRunAdmin)
admin.site.register(PesteringAttempt, PesteringAttemptAdmin)
admin.site.register(PesteringException, PesteringExceptionAdmin)
