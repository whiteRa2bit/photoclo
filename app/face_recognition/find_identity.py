from .models import Face
import numpy as np
import json


threshold = 0.8   # if we find a face, such that the distance between the found face and the given face
                # is smaller than a threshold, than we suppose it is the same avatar


def get_identity(face_id):
    face_input = Face.objects.filter(id=face_id).first()
    faces_query = Face.objects.filter(avatar__isnull=False)

    embedding_input = face_input['embedding']
    embedding_input = np.array(embedding_input)
    avatar_id = -1
    avatar_dist = float('Inf')

    for face in faces_query:
        next_embedding = face['embedding']
        next_embedding = np.array(next_embedding)
        norm = np.linalg.norm(embedding_input - next_embedding)
        if norm < avatar_dist:
            avatar_id = face['avatar']
            avatar_dist = norm

    if avatar_dist < threshold:
        return avatar_id
    else:
        pass  # It is necessary to call a function to create a new avatar here








