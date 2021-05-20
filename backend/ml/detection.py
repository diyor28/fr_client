import os

import cv2

from server import settings
from server.settings import config
from ml.utils import Detection


class FaceDetector:
	_net = None

	@classmethod
	def detect(cls, image, threshold=config.params_detection_threshold, size=(300, 300)):
		"""
		:type size: tuple
		:type image: np.ndarray
		:param size: tuple (w, h)
		:param image: BGR color space
		:param threshold: minimum confidence
		:return: list of coordinates [(x1, y1, x2, y2), (x1, y1, x2, y2)]
		"""
		if cls._net is None:
			config_path = os.path.join(settings.BASE_DIR, config.weights_detector_config)
			weights_path = os.path.join(settings.BASE_DIR, config.weights_detector)
			cls._net = cv2.dnn.readNetFromCaffe(config_path, weights_path)

		height, width = image.shape[:2]
		blob = cv2.dnn.blobFromImage(image.bgr, scalefactor=1.0, size=size, mean=[104, 117, 123],
									 swapRB=False, crop=False)
		cls._net.setInput(blob)
		predictions = cls._net.forward()
		detections = []
		predictions = predictions[0, 0]
		predictions = predictions[predictions[:, 2] > threshold]
		for prediction in predictions:
			x1 = int(prediction[3] * width)
			y1 = int(prediction[4] * height)
			x2 = int(prediction[5] * width)
			y2 = int(prediction[6] * height)
			if width > x2 > x1 > 0 and height > y2 > y1 > 0:
				bbox = (x1, y1, x2, y2)
				detections.append(Detection(bbox=bbox,
											confidence=prediction[2],
											image=image.crop(bbox=bbox)))
		return detections
