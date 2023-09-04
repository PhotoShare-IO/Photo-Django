from django.urls import path

from posts.views import PostsView

urlpatterns = [path("posts/", PostsView.as_view(), name="posts")]
