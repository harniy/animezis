from django import forms
from django.contrib import admin

from django.utils.safestring import mark_safe

from .models import Category, Actor, Genre, Movie, MovieShots, Serias, Profile, Comment, Rating

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


"""Категории"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Визуализирует поля в админке, в данном случае поле категории"""
    list_display = ("id", "name", "url")
    """Метод делает кликабельным имя фильма"""
    list_display_links = ("id", "name",)


# """Добавляем поля комментариев к нашим фильмам(Movie), что бы сразу видеть какие комменты у фильма есть"""
# class ReviewInLine(admin.TabularInline):
#     model = Reviews
#     extra = 1
#     readonly_fields = ("name", "email")

"""Добавляем поле кадров из фильма напрямую в Movie"""
class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)
    """Вывод изображения в админке, что бы вместо ссылки была картинка"""
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

    get_image.short_description = "Изображение"

class SeriasInline(admin.TabularInline):
    model = Serias
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1



"""Фильмы"""
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "time", "ongoing")
    """Метод создает фильтр, в данном варианте фильтруем по полю категорий и году выпуска,
    можно добавлять сколько угодно фильтров"""
    list_filter = ("year", "category",)
    """добавляем поиск в фильмах, здесь по названию и категории"""
    search_fields = ("title", "category__name")
    inlines = [SeriasInline, MovieShotsInline,CommentInline,]
    """Добавляем кнопку сохранить вверху сайта, что бы не листать вниз"""
    save_on_top = True
    form = MovieAdminForm




"""Актеры и режиссеры"""
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "get_image")

    """Вывод изображения в админке, что бы вместо ссылки была картинка"""
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

"""Жанры"""
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")



"""Кадры из фильма"""
@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")

    """Вывод изображения в админке, что бы вместо ссылки была картинка"""

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="55" height="55"')

    get_image.short_description = "Изображение"



@admin.register(Serias)
class SeriasAdmin(admin.ModelAdmin):
    list_display = ("name", "movie")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content',)
    """такой метод используется для полей ForeignKey"""
    search_fields = ("user__username", 'post__title', 'content')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'vote',)



admin.site.site_title = "Anime"
admin.site.site_header = 'Anime'

