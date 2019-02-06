# API
* /recognize - get all faces and their embeddings on a given photo
	* GET: url
		* returns JSON file with following fields:
          * "boxes" - detected faces coordinates, each box is a list of four integers [x1, y1, x2, y2] , where x1 < x2, y1 < y2
          * "confidence" - netework confidence, that detected face is indeed a face, float num from 0 to 1
          * "embeddings" - face encoding, each embedding is a list of 128 elements, where each num from -1 to 1
          * "faces_num" - total number of detected faces
