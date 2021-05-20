import os

from server import settings
from server.settings import config
from ml.model import WideResNet


class AgeGenderModel:
	_gender_model = None

	@classmethod
	def load_model(cls):
		if cls._gender_model is None:
			cls._gender_model = WideResNet(
				os.path.join(settings.BASE_DIR, config.weights_gendernet))

	@classmethod
	def predict_gender(cls, image):
		cls.load_model()
		return cls._gender_model.predict(image.bgr)
