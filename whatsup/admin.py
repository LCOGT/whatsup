from django.contrib import admin
from whatsup.models import Target

class TargetAdmin(admin.ModelAdmin):
    list_display = ['name','ra','dec','description','avm_desc']
    list_filter = ['avm_desc']

admin.site.register(Target,TargetAdmin)