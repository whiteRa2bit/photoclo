from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app.photo_load.views import PhotoView
from app.web.views import index
from .views import sign_in, sign_out, sign_up, test_api

router = routers.SimpleRouter()
router.register(r'api/photos', PhotoView, base_name='photos')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sign_in/', sign_in),
    path('api/sign_up/', sign_up),
    path('api/sign_out/', sign_out),
    path('api/test/', test_api),
    path('<path>', index),
    path('', index),
    path(r'', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
