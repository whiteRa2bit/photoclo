import os

import requests
from celery import Celery
from django.conf import settings

from app.face_recognition.serializers import FaceSerializer
from app.photo_load.models import Photo, Storage
from .find_identity import get_identity

app = Celery('tasks', broker='pyamqp://guest@localhost//')

with open(os.path.join(settings.BASE_DIR, 'face_recognition',
                       'face_detection.config')) as file:
    fd_url = file.readline()
    site_url = file.readline()


@app.task
def get_faces(photo_id):
    storage = Storage.objects.filter(photo=photo_id).first().z_size
    storage_url = '{0}{1}'.format(site_url, storage.url)
    data = requests.get(fd_url, params={'url': storage_url}).json()
    faces = [{'bounding_box': data['boxes'][i],
              'embedding': data['embeddings'][i],
              'photo': photo_id} for i in range(data['faces_num'])]
    if data['faces_num'] != 0:
        serializer = FaceSerializer(data=faces, many=True)
        if serializer.is_valid(raise_exception=True):
            faces = serializer.save()
            for face in faces:
                get_identity(face.id)
    photo = Photo.objects.filter(storage_id=photo_id).first()
    photo.checked = True
    photo.save()

