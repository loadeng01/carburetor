from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer
from rest_framework import permissions
from apps.car.permissions import IsAdminOrEmployee


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permissions.AllowAny(),
        return IsAdminOrEmployee(),

