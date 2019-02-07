from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from .models import Face, Avatar
from .serializers import FaceSerializer, AvatarSerializer


class FaceView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk):
        faces = Face.objects.filter(photo__owner=request.user).filter(photo=pk)
        if len(faces) == 0:
            return Response({}, status=HTTP_204_NO_CONTENT)
        answer = FaceSerializer(faces, many=True)
        return Response({'faces': answer}, status=HTTP_200_OK)

    def update(self, request, pk=None):
        new_avatar = request.data['new_avatar']
        face_id = request.data['face']
        face = Face.objects.filter(photo__owner=request.user)\
            .filter(face_id=face_id)
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
        avatars = Avatar.objects.filter(face__photo__owner=request.user)
        if len(avatars) == 0:
            return Response({}, status=HTTP_204_NO_CONTENT)
        answer = AvatarSerializer(avatars, many=True)
        return Response(answer, status=HTTP_200_OK)

    def create(self, request, pk=None):
        faces = Face.objects.filter(photo__owner=request.user)
        face = faces.filter(id=request.data['face_id'])
        name = request.data['name']

        avatar_serializer = AvatarSerializer(data={'name': name,
                                                   'face': face.id})

        if avatar_serializer.is_valid():
            new_avatar = avatar_serializer.save()
            return Response(new_avatar, status=HTTP_201_CREATED)
        else:
            return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        avatar = Avatar.objects.filter(face__photo__owner=request.user).\
            firter(id=pk)
        if len(avatar) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)
        avatar = avatar.first()

        new_name = request.data['new_name']
        avatar.name = new_name
        avatar.save()
        return Response({'updated_avatar': AvatarSerializer(avatar)},
                        status=HTTP_200_OK)

