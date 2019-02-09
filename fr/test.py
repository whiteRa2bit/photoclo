import requests
from detect_faces import *
import urllib.request
import cv2
import json
from flask import jsonify

# Comment this if you want to use file
'''
url = "https://pp.userapi.com/c849124/v849124518/1254d8/wD1_ZRhuszM.jpg"
resp = urllib.request.urlopen(url) 
img = np.asarray(bytearray(resp.read()), dtype="uint8") 
img = cv2.imdecode(img, cv2.IMREAD_COLOR)

# Comment this if you want to use url
'''
img_path = '/home/pavel/MyDocs/photoclo/pictures/test9.jpg'
img = cv2.imread(img_path)




faces = []
faces = get_faces(img)



for face in faces:
    cv2.rectangle(img, (face['rect'][0], face['rect'][1]), (face['rect'][2], face['rect'][3]), (0, 255, 0), 2)

'''
emb1 = np.array(faces1[0]['embedding'])
emb2 = np.array(faces2[0]['embedding'])
print("Norm is equal = ", np.linalg.norm(emb1-emb2))
'''
cv2.imshow("faces", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
