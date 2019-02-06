import tensorflow as tf
import facenet
import cv2
import imutils
import numpy as np
import argparse
from mtcnn.mtcnn import MTCNN

insize = 20
threshold = [0.6, 0.7, 0.7]
factor = 0.709
margin = 10
input_image_size = 160

sess = tf.Session()

facenet.load_model("model/model.pb")

images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]
detector = MTCNN()

def get_faces(img):
    faces = []
    #img = cv2.imread(img_path)
    imutils.resize(img,width=1000)
    result = detector.detect_faces(img)
    #print("Faces found:", len(result))
    faces_num = len(result)

    for i in range(faces_num):
        face = result[i]
        #print(face['confidence'])
        if face['confidence'] > 0.95:
            x, y, w, h = face['box']
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(x - margin / 2, 0)
            bb[1] = np.maximum(y - margin / 2, 0)
            bb[2] = np.minimum(x+w + margin / 2, img.shape[1])
            bb[3] = np.minimum(y+h + margin / 2, img.shape[0])
            cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
            resized = cv2.resize(cropped, (input_image_size,input_image_size),interpolation=cv2.INTER_CUBIC)
            prewhitened = facenet.prewhiten(resized)
        
            faces.append({'face':resized,'rect':[bb[0],bb[1],bb[2],bb[3]], 'confidence': face['confidence'], 'embedding':get_embedding(prewhitened)})
    return faces

def get_embedding(resized):
    reshaped = resized.reshape(-1,input_image_size,input_image_size,3)
    feed_dict = {images_placeholder: reshaped, phase_train_placeholder: False}
    # print(feed_dict)
    embedding = sess.run(embeddings, feed_dict=feed_dict)
    return embedding
