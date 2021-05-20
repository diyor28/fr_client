import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from ml.utils import VideoCaptureAsync
from server.models import CamerasModel


class FrameFeed:
	def __init__(self, stream):
		self.stream = stream

	def __iter__(self):
		while True:
			ret, frame = self.stream.read()
			if not ret:
				return self.__iter__()
			frame = cv2.imencode('.jpg', frame)[1].tostring()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	def __next__(self):
		ret, frame = self.stream.read()
		if not ret:
			return self.__next__()
		frame = cv2.imencode('.jpg', frame)[1].tostring()
		return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	def close(self):
		self.stream.release()


class StreamsView(CreateView):

	def get(self, request, *args, **kwargs):
		pk = int(kwargs.get("pk"))
		camera = get_object_or_404(CamerasModel, pk=pk)
		stream = VideoCaptureAsync(src=camera.full_url)
		return StreamingHttpResponse(FrameFeed(stream), 'multipart/x-mixed-replace; boundary=frame')
