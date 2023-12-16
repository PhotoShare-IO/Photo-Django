from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views, status
from django.shortcuts import get_object_or_404

from posts.models import PostModel
from posts.serializers import PostSerializer, PostCreateSerializer


class PostsView(views.APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["posts"],
        responses={200: PostSerializer()},
    )
    def get(self, request, pk=None):
        if pk:
            post = get_object_or_404(PostModel, pk=pk)
            serializer = PostSerializer(post)
        else:
            posts = PostModel.objects.all()
            serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

