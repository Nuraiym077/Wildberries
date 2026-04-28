from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version='v1',
        description="Документация для магазина",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API эндпоинты
    path('', include('store.urls')),  # Хорошая практика — добавлять префикс api/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Авторизация
    path('accounts/', include('allauth.urls')),
]

# Раздача медиа и статики при разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)