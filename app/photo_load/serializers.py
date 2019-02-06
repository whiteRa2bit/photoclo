from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Photo, Storage

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD)


class StorageSerializer(serializers.ModelSerializer):
    o_size = serializers.ImageField(required=False)

    class Meta:
        model = Storage
        fields = ('original', 'o_size')

    def create(self, validated_data):
        print(validated_data)
        storage, created = \
            Storage.objects.update_or_create(original=validated_data[0])
        return storage


class PhotoSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    storage = StorageSerializer(required=False)

    class Meta:
        model = Photo
        fields = ('owner', 'storage', 'width', 'height')

    def create(self, validated_data):
        storage_data = validated_data.pop('storage')
        storage = StorageSerializer.create(StorageSerializer(),
                                           validated_data=storage_data)

        photo, created = \
            Photo.objects.update_or_create(owner=validated_data.pop('user')[0],
                                           storage=storage)
        return photo
