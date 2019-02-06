from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from .models import Photo, Storage
from .serializers import PhotoSerializer


class PhotoView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk=None):
        offset = int(request.query_params['offset'])
        limit = int(request.query_params['limit'])
        size = request.query_params['size']
        user = request.user

        photos = Photo.objects.filter(owner=user)\
                      .order_by('-time_created')[offset:offset + limit]

        size_field = Storage._meta.get_field('{0}_size'.format(size))
        client_photo = [{'url': size_field.value_from_object(
                                Storage.objects.filter(photo=photo)[0]).url,
                         'height': photo.height, 'width': photo.width,
                         'id': photo.storage.id}
                        for photo in photos]

        count = len(client_photo)
        return Response({'count': count, 'photos': client_photo},
                        status=HTTP_200_OK)

    def retrieve(self, request, pk):
        photos = Photo.objects.filter(owner=request.user)
        photo = Storage.objects.filter(photo__in=photos).filter(photo=pk)

        if len(photo) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)

        return Response({'url': photo[0].o_size.url}, status=HTTP_200_OK)

    def destroy(self, request, pk):
        photos = Photo.objects.filter(owner=request.user)
        photo = Storage.objects.filter(photo__in=photos).filter(photo=pk)

        if len(photo) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)

        photo[0].delete()
        return Response(status=HTTP_200_OK)

    def create(self, request, pk=None):
        data = request.data
        status_list = []
        for item in request.data.getlist('items[]'):
            data['storage'] = item
            data['owner'] = request.user.id
            data['user'] = request.user

            photo_serializer = PhotoSerializer(data=data)

            if photo_serializer.is_valid():
                photo_serializer.create(validated_data=data)
                status_list.append('Success')
            else:
                status_list.append('Nope')
        return Response({'status': status_list}, HTTP_201_CREATED)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        photos = Photo.objects.filter(owner=request.user)
        photo = Storage.objects.filter(photo__in=photos).filter(photo=pk)

        if len(photo) == 0:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response({'url': photo[0].original.url}, status=HTTP_200_OK)

