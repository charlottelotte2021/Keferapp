from django.contrib import admin
from .models import Notification, Post, UserProfile, ThreadModel

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(ThreadModel)
admin.site.register(Notification)
# admin.site.register(Address)
