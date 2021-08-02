from django import template
import random
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from movies.models import Category, Movie, Genre, Profile
register = template.Library()



@register.inclusion_tag('movies/tags/category_movie.html')
def get_categories():
    """Вывод всех категорий"""
    category = Category.objects.all()
    return {'categories': category}

@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies():
    movies = Movie.objects.order_by("-time")[:5]
    return {"last_movies": movies}

@register.inclusion_tag('movies/tags/genre_movie.html')
def get_genre():
    genre = Genre.objects.order_by("name")
    return {"genre_list": genre}


@register.inclusion_tag('movies/tags/slider.html')
def get_slider():
    slider = Movie.objects.order_by('-time').filter(ongoing=True)[:20]
    return {'slider': slider}


@register.inclusion_tag('movies/tags/random_movie.html')
def get_random():
    anime = Movie.objects.all()
    anime_random = len(anime)
    random_list = []
    for i in range(anime_random):
        i += 2
        random_list.append(i)
    random_id = random.choice(random_list)

    anime_2 = Movie.objects.order_by("id")
    anime_random_2 = len(anime_2)
    random_list_2 = []
    for i in range(anime_random_2):
        i += 2
        random_list_2.append(i)
    exept_choice = random.choice(random_list_2)

    try:
        anime_ran = anime.get(id=random_id)
    except:
        anime_ran = anime.get(id=exept_choice)
    return {'anime_ran': anime_ran}


@register.simple_tag
def get_avatar(Profile, comment):
    return Profile.__class__.objects.get(user=comment.user.id).avatar.url


