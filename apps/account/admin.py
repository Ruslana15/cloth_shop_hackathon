from django.contrib import admin
from django.contrib.auth import get_user_model


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active')


admin.site.register(get_user_model())

# admin.site.site_title = 'Django Shop'
# admin.site.site_header = 'Django Shop'