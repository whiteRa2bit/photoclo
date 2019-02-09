from rest_framework import serializers

from .models import Avatar, Face


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('id', 'name',)


class FaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Face
        fields = ('id', 'avatar', 'photo', 'embedding', 'bounding_box',
                  'user_checked')
