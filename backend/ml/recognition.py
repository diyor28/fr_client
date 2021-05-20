import os

from server import settings
from server.settings import config
from ml.detection import FaceDetector
from ml.model import FaceNetModel
from ml.utils import Image


class FaceRecognition:
	_facenet_model = None
	_gender_model = None

	@classmethod
	def load_model(cls):
		if cls._facenet_model is None:
			cls._facenet_model = FaceNetModel(
				weights_dir=os.path.join(settings.BASE_DIR, config.weights_facenet))

	@classmethod
	def extract_vector(cls, file):
		if isinstance(file, Image):
			image = file.copy()
		else:
			image = Image(file)
		detections = FaceDetector.detect(image=image)  # BGR
		result = []

		for detection in detections:
			cropped_face = image.crop(bbox=detection.bbox)
			vector = cls.face2vector(face_image=cropped_face, return_list=True)
			result.append(dict(confidence=detection['confidence'],
							   vector=vector, image=cropped_face))
		return result

	@classmethod
	def face2vector(cls, face_image, return_list=False):
		"""
		:param face_image: in BGR color space
		:param return_list: If True return type "list" else return type "np.ndarray"
		:return: 512 dimensional vector
		"""

		cls.load_model()

		vector = cls._facenet_model.predict(face_image.rgb)
		if return_list:
			return list(vector.astype(float))
		return vector

	@classmethod
	def faces2vector(cls, face_images, return_list=False):
		"""
		:param face_images: list of images in RGB color space
		:param return_list: If True return "list" else return "np.ndarray"
		:return: 128 dimensional vector
		"""
		cls.load_model()

		prediction = cls._facenet_model.predict_multiple([e.rgb for e in face_images])
		if return_list:
			return [list(element) for element in prediction.astype(float)]
		return prediction
