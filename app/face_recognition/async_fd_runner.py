import asyncio

import requests
from celery import Celery

from app.face_recognition.serializers import FaceSerializer
from app.photo_load.models import Photo, Storage

app = Celery('tasks', broker='pyamqp://guest@localhost//')

loop = asyncio.get_event_loop()
with open('face_detection.config') as file:
    fd_url = file.readline()
    site_url = file.readline()


@app.task
def get_faces(photo_id):
    storage = Storage.objects.filter(photo=photo_id).first().z_size
    storage_url = '{0}{1}'.format(site_url, storage.url)
    print(storage_url)
    data = requests.get(fd_url, params={'url': storage_url}).json()
    faces = [{'bounding_box': data['boxes'][i],
              'embedding': data['embeddings'][i],
              'photo': photo_id} for i in range(data['faces_num'])]
    if data['faces_num'] != 0:
        serializer = FaceSerializer(data=faces, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    photo = Photo.objects.filter(storage_id=photo_id).first()
    photo.checked = True
    photo.save()

