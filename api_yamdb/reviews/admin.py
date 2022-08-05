from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryGengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')


admin.site.register(Category, CategoryGengeAdmin)
admin.site.register(Genre, CategoryGengeAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
