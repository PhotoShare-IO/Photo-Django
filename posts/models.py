from django.db import models
from django.contrib.auth import get_user_model
from utils.models import CreateDatetimeModel
from utils.functions import truncate_long_text


class AlbumModel(CreateDatetimeModel):
    name = models.CharField(
        "Album name", max_length=90, null=False, blank=False
    )
    description = models.TextField("Album description", blank=True, null=True)

    def get_posts(self):
        return self.posts.all()


class PostModel(CreateDatetimeModel):
    album = models.ForeignKey(
        AlbumModel,
        verbose_name="Album",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    file_url = models.URLField("Content URL", blank=False, null=False)
    name = models.CharField(
        "Post title", blank=False, null=False, max_length=90
    )
    description = models.TextField(
        "Description for post", blank=True, null=True
    )

    def get_anount_of_likes(self) -> int:
        return self.likes.all().count()

    def get_comments(self):
        return self.comments.all()


class CommentModel(CreateDatetimeModel):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="Comment author",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        PostModel,
        verbose_name="Comment to post",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField("Comment text", blank=False, null=False)

    def get_comment_author(self) -> str:
        return self.user.username

    def __str__(self) -> str:
        return f"POST: {truncate_long_text(self.post.name)} - FROM {self.user.username}: {truncate_long_text(self.text)}"


class LikeModel(CreateDatetimeModel):
    post = models.ForeignKey(
        PostModel, verbose_name="Liked post", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="Who likes",
        on_delete=models.CASCADE,
        related_name="likes",
    )
