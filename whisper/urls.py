from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from main.views import activate_email, reset_password, test_view
from rest_framework import permissions  # new

schema_view = get_schema_view(
    openapi.Info(
        title="EDM API",
        default_version="v1",
        description="Test API",
        terms_of_service="",
        contact=openapi.Contact(email="desmond@getmobile.tech"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('activate/', activate_email, name='activate'),
    path('test/', test_view, name='test'),
    path('password/reset/confirm/', reset_password, name='reset_password'),
    path('whisper/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
