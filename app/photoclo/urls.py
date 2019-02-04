from django.contrib import admin
from django.urls import path

from app.web.views import index
from .views import sign_in, sign_out, sign_up, test_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sign_in/', sign_in),
    path('api/sign_up/', sign_up),
    path('api/sign_out/', sign_out),
    path('api/test/', test_api),
    path('<path>', index),
    path('', index),
]
