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
img_path = '/home/pavel/MyDocs/photoclo/pictures/test17.jpg'
img = cv2.imread(img_path)




faces = []
faces = get_faces(img)

bounding_boxes = []
confidence = []
embeddings = []

for face in faces:
    bounding_boxes.append([int(_) for _ in face['rect']])
    confidence.append(face['confidence'])
    embeddings.append([float("{0:.8f}".format(_)) for _ in face['embedding'][0]])
data = {"faces_num": len(faces), "boxes": bounding_boxes, "embeddings": embeddings, "confidence": confidence}
tmp = json.dumps(data, indent = 4)
print(tmp)

print(json.loads(tmp))
embedding = json.loads(tmp)['embeddings'][0]
print(embedding)


for face in faces:
    cv2.rectangle(img, (face['rect'][0], face['rect'][1]), (face['rect'][2], face['rect'][3]), (0, 255, 0), 2)



cv2.imshow("faces", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
