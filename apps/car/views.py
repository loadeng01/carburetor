from rest_framework.decorators import action
from rest_framework import permissions
from .models import Car
from .serializers import *
from .permissions import IsAuthorOrAdminOrEmployee
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from apps.favorite.models import Favorite
from django.contrib.auth import get_user_model
from ..account.serializers import UserSerializer, UserListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.favorite.serializers import FavoriteSerializer

User = get_user_model()


class Pagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', )
    filterset_fields = ('category', 'year')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        return CarSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return IsAuthorOrAdminOrEmployee(),
        elif self.request.method == 'POST':
            return permissions.IsAuthenticated(),
        return permissions.AllowAny(),

    @action(['POST', 'DELETE', 'GET'], detail=True)
    def favorites(self, request, pk):
        car = self.get_object()
        user = request.user

        if request.method == 'POST':
            if user.favorites.filter(car=car).exists():
                return Response('This post is already in favorites', status=400)
            Favorite.objects.create(car=car, owner=user)
            return Response('Added to favorites', status=201)

        elif request.method == 'GET':
            users = car.favorites.all().values('owner')
            favorites_users = User.objects.filter(id__in=users)
            serializer = UserListSerializer(favorites_users, many=True)
            return Response(serializer.data)

        else:
            favorite = user.favorites.filter(car=car)
            if favorite.exists():
                favorite.delete()
                return Response('Deleted from favorites', status=204)
            return Response('Post not found', status=404)


class UserFavoritesView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(owner=user)
        data = []
        for item in favorites:
            serializer = CarListSerializer(item.car)
            data.append(serializer.data)

        return Response(data, status=200)
