from django.contrib import admin
from django.contrib.auth import get_user_model


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(get_user_model(), UserAdmin)

admin.site.site_title = 'Django Shop'
admin.site.site_header = 'Django Shop'