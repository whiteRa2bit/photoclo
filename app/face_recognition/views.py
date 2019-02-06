from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from app.photo_load.models import Photo
from .models import Face, Avatar
from .serializers import FaceSerializer, AvatarSerializer


class FaceView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk):
        photos = Photo.objects.filter(owner=request.user)
        faces = Face.objects.filter(photo__in=photos).filter(photo=pk)
        if len(faces) == 0:
            return Response({}, status=HTTP_204_NO_CONTENT)
        answer = FaceSerializer(faces, many=True)
        return Response(answer, status=HTTP_200_OK)

    def update(self, request, pk):
        new_avatar = request.data['new_avatar']
        face_id = request.data['face']
        photos = Photo.objects.filter(owner=request.user)
        face = Face.objects.filter(photo__in=photos).filter(face_id=face_id)
        if len(face) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)
        face = face.first()
        face.avatar = Avatar.objects.filter(id=new_avatar)
        face.save()
        return Response({'new_face': FaceSerializer(face)},
                        status=HTTP_200_OK)


class AvatarView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk=None):
        photos = Photo.objects.filter(owner=request.user)
        faces = Face.objects.filter(photo__in=photos)
        avatars = Avatar.objects.filter(face__in=faces)
        if len(avatars) == 0:
            return Response({}, status=HTTP_204_NO_CONTENT)
        answer = AvatarSerializer(avatars, many=True)
        return Response(answer, status=HTTP_200_OK)

    def update(self, request, pk):
        photos = Photo.objects.filter(owner=request.user)
        faces = Face.objects.filter(photo__in=photos)
        avatar = Avatar.objects.filter(face_in=faces).filter(id=pk)
        if len(avatar) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)
        avatar = avatar.first()

        new_name = request.data['new_name']
        avatar.name = new_name
        avatar.save()
        return Response({'new_avatar': AvatarSerializer(avatar)},
                        status=HTTP_200_OK)

