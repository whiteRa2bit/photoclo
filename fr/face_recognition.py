from flask import Flask, request
from flask import jsonify
import requests
from detect_faces import *
import urllib.request

app = Flask(__name__)

@app.route('/recognize', methods = ['GET'])
def return_faces():
	url = request.args['url']  # user provides url in query string
	resp = urllib.request.urlopen(url) 
	img = np.asarray(bytearray(resp.read()), dtype="uint8") 
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	#img = '/home/pavel/MyDocs/photoclo/pictures/test9.jpg'
	faces = []
	faces = get_faces(img)
	bounding_boxes = []
	confidence = []
	embeddings = []
	for face in faces:
		bounding_boxes.append([int(_) for _ in face['rect']])
		confidence.append(face['confidence'])
		embeddings.append([float("{0:.8f}".format(_)) for _ in  face['embedding'][0]])
	return jsonify({"faces_num":len(faces), "boxes":bounding_boxes, "embeddings":embeddings, "confidence":confidence})
