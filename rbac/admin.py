from django.contrib import admin

# Register your models here.

from rbac import models

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id','title','url','menus']
    list_editable = ['title','url','menus']

admin.site.register(models.UserInfo)
admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Menu)


