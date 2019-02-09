from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_409_CONFLICT,
)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sign_in(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Требуется пароль и логин.'},
                        status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Неправильный пароль или логин.'},
                        status=HTTP_404_NOT_FOUND)

    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if username is None or password is None or email is None:
        return Response(
            {'error': 'Требуется логин, пароль и почта.'},
            status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь с таким именем сущесвует.'},
                        status=HTTP_409_CONFLICT)

    user = User.objects.create_user(username=username, password=password,
                                    email=email)

    if not user:
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def sign_out(request):
    logout(request)
    return Response(status=HTTP_200_OK)
