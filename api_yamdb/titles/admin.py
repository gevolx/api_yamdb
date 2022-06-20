from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    # list_display = ()
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # list_display = ()
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ()
    pass
