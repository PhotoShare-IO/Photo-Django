from django.urls import path

from posts.views import PostsView

urlpatterns = [
    path("posts/", PostsView.as_view(), name="posts"),
    path("post/<int:pk>", PostsView.as_view(), name="post"),
    path("post/create", PostsView.as_view(), name="post_create"),
]
