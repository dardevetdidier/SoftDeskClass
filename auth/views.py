from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth.serializers import RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    serializer = RegisterSerializer(request.data)
    serializer.validate(request.data)
    serializer.create(request.data)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
