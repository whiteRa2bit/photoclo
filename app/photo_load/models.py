import sys
from datetime import datetime
from io import BytesIO
from uuid import uuid4

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

sizes = {'o': 'max', 'z': 1080, 'y': 807, 'x': 604, 'm': 130, 's': 100}


def get_upload_path(instance, filename):
    return instance.get_upload_path(filename)


def get_upload_path_size_o(instance, filename):
    return instance.get_upload_path("o_{0}".format(filename))


def get_upload_path_size_z(instance, filename):
    return instance.get_upload_path("z_{0}".format(filename))


def get_upload_path_size_y(instance, filename):
    return instance.get_upload_path("y_{0}".format(filename))


def get_upload_path_size_x(instance, filename):
    return instance.get_upload_path("x_{0}".format(filename))


def get_upload_path_size_m(instance, filename):
    return instance.get_upload_path("m_{0}".format(filename))


def get_upload_path_size_s(instance, filename):
    return instance.get_upload_path("s_{0}".format(filename))


class Storage(models.Model):
    original = models.ImageField(upload_to=get_upload_path)
    o_size = models.ImageField(upload_to=get_upload_path_size_o)
    z_size = models.ImageField(upload_to=get_upload_path_size_z)
    y_size = models.ImageField(upload_to=get_upload_path_size_y)
    x_size = models.ImageField(upload_to=get_upload_path_size_x)
    m_size = models.ImageField(upload_to=get_upload_path_size_m)
    s_size = models.ImageField(upload_to=get_upload_path_size_s)

    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(*args, **kwargs)
        self.salt = uuid4().hex

    def get_upload_path(self, filename):
        return '{0}/{1}'.format(self.salt, filename)

    def save(self, *args, **kwargs):
        if not self.id:
            self.o_size = self.compress(self.original, 'o')
            self.z_size = self.compress(self.original, 'z')
            self.y_size = self.compress(self.original, 'y')
            self.x_size = self.compress(self.original, 'x')
            self.m_size = self.compress(self.original, 'm')
            self.s_size = self.compress(self.original, 's')

        super(Storage, self).save(*args, **kwargs)

    def compress(self, file, size):
        image_temp = Image.open(file)
        output_io_stream = BytesIO()
        if size == 'o':
            shape = image_temp.size
        else:
            shape = (min(image_temp.width, sizes[size]),
                     min(image_temp.height, sizes[size]))
        image_temp.thumbnail(shape)
        image_temp.save(output_io_stream, format='JPEG', quality=90)
        output_io_stream.seek(0)
        sized = \
            InMemoryUploadedFile(output_io_stream, 'ImageField',
                                 "{0}.jpeg".format(file.name.split('.')[0]),
                                 'image/jpeg', sys.getsizeof(output_io_stream),
                                 None)
        return sized


class Photo(models.Model):
    storage = models.OneToOneField(Storage, on_delete=models.CASCADE,
                                   primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField()
    width = models.IntegerField()
    height = models.IntegerField()

    def save(self, *args, **kwargs):
        image_temp = Image.open(self.storage.original)
        if image_temp._getexif() is not None and \
                image_temp._getexif().get(36867, None) is not None:
            self.time_created = datetime.strptime(
                image_temp._getexif()[36867], '%Y:%m:%d %H:%M:%S')

        else:
            self.time_created = datetime.now()
        self.width, self.height = image_temp.size
        super(Photo, self).save(*args, **kwargs)
