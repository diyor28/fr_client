import argparse

import cv2
import numpy as np
from utils import (FaceRecognition, FaceDetector, ObjectTracker)
from server.settings import config

from ml.utils import Image


class CameraReader:
	debug = False
	info = False
	tracker = ObjectTracker()

	@classmethod
	def plot(cls, image, text, point):
		x1, y1 = point
		text_x = max(0, x1 - 50)
		text_y = y1
		cv2.putText(image, text=text, org=(text_x, text_y),
					fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=1, color=(255, 160, 255), thickness=2, lineType=cv2.LINE_AA)

	@classmethod
	def run(cls):
		FaceRecognition.load_model()
		video = cv2.VideoCapture("test1.mp4")
		writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, video.read()[1][:2])
		prev_frame = None
		while True:
			ret, frame = video.read()

			if frame is None:
				continue

			frame = Image(frame, color_space="BGR")

			if cls.debug:
				cv2.imshow("Stream", frame)

			if prev_frame is not None:
				change = np.linalg.norm(prev_frame - cv2.GaussianBlur(frame.bgr.mean(axis=-1), (9, 9), 0) / 255)
				if change < config.params_max_change:
					# time.sleep(DETECTION_TIMEOUT)
					continue

			prev_frame = cv2.GaussianBlur(frame.bgr.mean(axis=-1), (9, 9), 0) / 255

			detections = FaceDetector.detect(frame)

			detections = cls.tracker.update(detections)

			# for detection in detections:
			# 	detection.

			if not detections:
				print("")
				continue

			writer.write(frame)
		cv2.destroyAllWindows()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", default="false", choices=("True", "true", "1", "False", "false", "0"))
	parser.add_argument("--info", default="false", choices=("True", "true", "1", "False", "false", "0"))
	args = parser.parse_args()
	debug = (args.debug in ("true", "True", "1"))
	info = (args.info in ("true", "True", "1"))
	CameraReader.info = info
	CameraReader.debug = debug
	CameraReader.run()
