from django.contrib import admin

from .models import GlobalTheme, LocalThemeTree

admin.site.register(GlobalTheme)

admin.site.register(LocalThemeTree)

# Register your models here.
