from django.urls import path
from blog.views import index, post, page
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/', page, name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
