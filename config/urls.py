from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.category.views import CategoryViewSet
from apps.account.views import UserViewSet
from apps.car.views import CarViewSet, UserFavoritesView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
   openapi.Info(
      title="CARS API",
      default_version='v1',
   ),
   public=True,
)

router = SimpleRouter()
router.register('category', CategoryViewSet)
router.register('cars', CarViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('api/account/', include('apps.account.urls')),
    path('api/', include(router.urls)),
    path('api/account/cars/', UserFavoritesView.as_view()),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
