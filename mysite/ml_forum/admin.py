from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'name', 'surname', 'messages_count', 'time_create', 'biography', 'email', 'is_public')
    list_display_links = ('id', 'name', 'email')
    search_fields = ('user', 'name', 'surname', 'biography', 'email', 'is_public')


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topics_count', 'time_create', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'section', 'name', 'posts_count', 'time_create', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('user', 'name', 'section')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'topic', 'post', 'time_create', 'is_published')
    list_display_links = ('id', 'post')
    search_fields = ('user', 'topic', 'post')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)