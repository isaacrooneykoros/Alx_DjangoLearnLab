from django.contrib import admin
from .models import Profile, Post

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
admin.site.register(Post)
admin.site.register(Profile)