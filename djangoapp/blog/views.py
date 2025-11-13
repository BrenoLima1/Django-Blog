from typing import Any
from blog.models import Page, Post, Tag, Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title' : 'Home - ',
        })

        return context

class CreatedByListView(PostListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = PER_PAGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._temp_context = {}   # inicializa corretamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(pk=self.kwargs['author_pk']).first()

        if user is None:
            raise Http404()

        if user.first_name or user.last_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        else:
            user_full_name = user.username

        page_title = f'posts de {user_full_name} - '

        context.update({
            'page_title': page_title,
            'user': user,  # já pode passar o user aqui
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(created_by__pk=self.kwargs['author_pk'])

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs['author_pk']
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            return redirect('blog:index')

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)

class CategoryListView(PostListView):
    allow_empty = True
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = PER_PAGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._temp_context = {}

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return Post.objects.filter(category=category).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        context.update({
            'page_title': f'Categoria {category.name} - ',
            'category': category,
        })
        return context

class TagListView(PostListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = PER_PAGE

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        # garante que a tag existe
        self.tag_obj = get_object_or_404(Tag, slug=slug)
        # retorna apenas os posts publicados com essa tag
        return Post.objects.get_published().filter(tags__slug=slug).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.tag_obj.name} posts - ' if self.tag_obj else 'Home - '
        context.update({
            'page_title': page_title,
            'tag': self.tag_obj,
        })
        return context

class SearchListView(PostListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = PER_PAGE

    def get_queryset(self):
        # pega o valor da busca da querystring
        self.search_value = self.request.GET.get('search', '').strip()
        queryset = Post.objects.get_published()

        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) |
                Q(excerpt__icontains=self.search_value) |
                Q(content__icontains=self.search_value)
            )

        return queryset.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = (
            f'Resultados para "{self.search_value}" - '
            if self.search_value else 'Home - '
        )
        context.update({
            'page_title': page_title,
            'search_value': self.search_value,
        })
        return context



class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # garante que só páginas publicadas aparecem
        return Page.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - '
        return context



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} - '
        return context
