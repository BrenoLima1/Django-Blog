from django.urls import path
from blog.views import created_by, index, post, page, category
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('created_by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
