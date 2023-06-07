from rest_framework import views
from rest_framework.response import Response

from .models import DumbModel
from .serializers import DumbSerializer

# Create your views here.

class DumbView(views.APIView):
    
    def get(self, request,*args, **kwargs):
        return Response(DumbSerializer(DumbModel.objects.all(), many=True).data)