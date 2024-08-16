from django.contrib import admin
from firstapp.models import Category, Post

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'category', 'img_url', 'created_at', 'updated_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)