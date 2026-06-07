from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('register/',views.register),
    path('addpost/',views.add_post),
    path('viewpost/',views.view_post),
    path('profile/<int:id>/',views.view_profile),
    path('editpost/<int:id>/',views.edit_post),
    path('editedpost/<int:id>/',views.get_post),
    path('deletepost/<int:id>/',views.delete_post),
    path('comments/',views.comments),
    path('viewcmmt/<int:id>/',views.view_comments),
    path('aihelper/',views.content_helper),
    path('search/',views.search_posts),
    path('singlepost/<int:id>/',views.single_post),
    path('like/<int:id>/',views.like_post),
    path('likecount/<int:id>/',views.like_count),
]