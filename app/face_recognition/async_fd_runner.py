import requests
from celery import Celery
from django.conf import settings

from app.face_recognition.serializers import FaceSerializer
from app.photo_load.models import Photo, Storage, sizes
from .find_identity import get_identity

app = Celery('tasks', broker='pyamqp://guest@localhost//')

fd_url = settings.FACE_DETECTION_URLS['face detection url']
site_url = settings.FACE_DETECTION_URLS['compressed photo storage']


@app.task
@app.task
def get_faces(photo_id):
    storage = Storage.objects.filter(photo=photo_id).first().z_size
    storage_url = '{0}{1}'.format(site_url, storage.url)
    data = requests.get(fd_url, params={'url': storage_url}).json()
    faces = [{'bounding_box': data['boxes'][i],
              'embedding': data['embeddings'][i],
              'photo': photo_id} for i in range(data['faces_num'])]
    faces = get_new_bounding_boxes(photo_id, faces)
    if data['faces_num'] != 0:
        serializer = FaceSerializer(data=faces, many=True)
        if serializer.is_valid(raise_exception=True):
            faces = serializer.save()
            for face in faces:
                get_identity(face.id)
    photo = Photo.objects.filter(storage_id=photo_id).first()
    photo.checked = True
    photo.save()


def get_new_bounding_boxes(photo_id, faces):
    photo = Photo.objects.filter(id=photo_id).first()
    h = photo.height
    w = photo.width
    if h <= w and h > sizes['z']:
        coef = h / sizes['z']
        for i in range(len(faces)):
            faces[i]['bounding_box'] = faces[i]['bounding_box'] * coef
    elif w <= h and w > sizes['z']:
        coef = w / sizes['z']
        for i in range(len(faces)):
            faces[i]['bounding_box'] = faces[i]['bounding_box'] * coef
    return faces

