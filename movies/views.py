from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Movie, Category, Genre, Comment
from .forms import CustomerForm, CommentForm, RatingForm
from django.db.models import Q


# def blog_post(request, post_id):
#     #your code
#     blog_object = Movie.objects.get(id=post_id)
#     blog_object.views = blog_object.views + 1
#     blog_object.save()
#     #your code
# def get_genres(self):
#     return Genre.objects.all()
class GenreYear:
    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.all()

    def get_caategory(self):
        return Category.objects.all()

    def get_slider(self):
        return Movie.objects.all()


def like_post(request):
    movie = get_object_or_404(Movie, id=request.POST.get('post_id'))
    """Фильтр для показа кнопки лайк-если пользователь не поставил его и дизлайк, что бы убрать лайк"""
    is_liked = False
    if movie.likes.filter(id=request.user.id).exists():
        movie.likes.remove(request.user)
        is_liked = False
    else:
        movie.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(movie.get_absolute_url())


def accountSettings(request):
    profile = request.user.profile
    form = CustomerForm(instance=profile)
    user_comments = Comment.objects.order_by('-id').filter(user=request.user.id)
    """Пагинация"""
    p = Paginator(user_comments, 15)
    page_num = request.GET.get('page')

    try:
        page = p.page(page_num)
    except:
        page = p.page(1)
    """добавление аватарки"""
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    context = {'form': form, 'user_comments': page}
    return render(request, 'account/profile.html', context)


class MoviesView(ListView):
    """Список аниме"""
    model = Movie
    # queryset = Movie.objects.all()  - вывод всех объектов из Movie
    """Вывод всех записей, кроме тех, что помечены как черновик, в данном случае это поле draft
    оно находится в Models.py class Movie и там поле draft"""
    queryset = Movie.objects.order_by("-time").filter(draft=False)
    template_name = 'movies/movies.html'
    paginate_by = 15



class MovieDetailView(DetailView):
    """Полное описание аниме"""
    model = Movie
    slug_field = 'url'
    template_name = 'movies/moviesingle.html'

    def get(self, request, slug):
        form = CommentForm()
        form_rating = RatingForm()
        movie = Movie.objects.get(url=slug)

        """Избранное"""
        is_favorite = False
        if movie.favor.filter(id=request.user.id).exists():
            is_favorite = True

        """Фильтр, который показывает кнопку лайк и дизлайк, если лайк поставил"""
        is_liked = False
        if movie.likes.filter(id=request.user.id).exists():
            is_liked = True

        """Количество просмотров на странице"""
        movie.views += 1
        movie.save()
        context = {
            'movie': movie,
            'form': form,
            'form_rating': form_rating,
            'is_favorite': is_favorite,
            'is_liked': is_liked,
            'total_likes': movie.total_likes(),

        }
        return render(request, 'movies/moviesingle.html', context)

    def post(self, request, slug):
        form = CommentForm()
        movie = Movie.objects.get(url=slug)

        """Комментарии"""
        if request.method == 'POST':
            form = CommentForm(request.POST or None)
            if form.is_valid():
                content = request.POST.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=movie, user=request.user, content=content, reply=comment_qs)
                comment.save()
                return HttpResponseRedirect(movie.get_absolute_url())
            else:
                form = CommentForm()

        context = {'form': form}
        return render(request, 'movies/moviesingle.html', context)


def favourite_list(request):
    user = request.user
    favourite_post = Movie.objects.order_by('-time').filter(favor=user.id)
    """Пагинация"""
    p = Paginator(favourite_post, 15)
    page_num = request.GET.get('page')
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'favourite_posts': page}
    return render(request, 'movies/favourite_list.html', context)

def like_list(request):
    user = request.user
    like_content = Movie.objects.order_by('-time').filter(likes=user.id)
    """Пагинация"""
    p = Paginator(like_content, 15)
    page_num = request.GET.get('page')
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)
    context = {'like_content': page}
    return render(request, 'movies/like_posts.html', context)

def favourite_post(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.favor.filter(id=request.user.id).exists():
        movie.favor.remove(request.user)
    else:
        movie.favor.add(request.user)
    return HttpResponseRedirect(movie.get_absolute_url())

def rating_form(request):
    movie = get_object_or_404(Movie, id=request.POST.get('post_id'))
    form = RatingForm(auto_id=True)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post_id = request.POST.get('post_id')
            instance.save()

    return HttpResponseRedirect(movie.get_absolute_url())

"""Генерируем ссылки к каждой категории"""


class CategoryModel(MoviesView, ListView):
    model = Movie
    queryset = Movie.objects.all()
    context_object_name = 'category_model'
    template_name = 'movies/movie_category.html'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов по годам"""
    template_name = 'movies/movies.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = Movie.objects.order_by('-id').filter(
            year__in=self.request.GET.getlist("year")).distinct()

        return queryset

    """Для ссылок, когда делаем пагинацию"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        return context


class FilterGenre(GenreYear, ListView):
    """Фильтр фильмов по жанрам"""
    template_name = 'movies/movies.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = Movie.objects.order_by('-id').filter(
            genres__in=self.request.GET.getlist("genre"))

        return queryset

    """Для ссылок, когда делаем пагинацию"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class FilterCategory(GenreYear, ListView):
    """Фильтр фильмов по жанрам"""
    template_name = 'movies/movies.html'
    paginate_by =15

    def get_queryset(self):
        queryset = Movie.objects.order_by('-id').filter(
            category__in=self.request.GET.getlist("category"))
        return queryset

    """Для ссылок, когда делаем пагинацию"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context


class Search(ListView):
    """Поиск фильмов"""
    template_name = 'movies/movies.html'
    paginate_by = 21

    def get_queryset(self):
        return Movie.objects.order_by("-id").filter(
            Q(title__icontains=self.request.GET.get('q')) | Q(description__icontains=self.request.GET.get('q')) | Q(search__icontains=self.request.GET.get('q')))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class Slider(ListView):
    template_name = 'movies/movies.html'
    model = Movie
    queryset = Movie.objects.order_by("-id").filter(ongoing=True)


class RandomAnime(ListView):
    model = Movie
    slug_field = 'url'
    template_name = 'movies/moviesingle.html'
    queryset = Movie.objects.all()


class LastUpdate(ListView):
    model = Movie
    template_name = 'movies/last_update.html'
    queryset = Movie.objects.order_by("-time")
    paginate_by = 15
