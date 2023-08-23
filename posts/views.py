from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views

from posts.models import PostModel
from posts.serializers import PostSerializer


class PostsView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["posts"],
        responses={200: PostSerializer()},
    )
    def get(self, request):
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
