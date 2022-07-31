from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from users.models import User
from api.serializers import UserSerializer, SingUpSerializer
from api.permissions import AdminOnly
from api_yamdb.settings import EMAIL_FOR_AUTH_LETTERS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username')
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOnly,)


@api_view(['POST'])
def signup(request):
    serializer = SingUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=request.data['username'],
        email=request.data['email']).exists():
        serializer.save()
    user = User.objects.get(username=request.data['username'],
        email=request.data['email'])
    token = default_token_generator.make_token(user)
    send_mail('Код подтверждения',
        token,
        EMAIL_FOR_AUTH_LETTERS,
        [request.data['email']],
        fail_silently=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
