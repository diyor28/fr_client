from multiprocessing import Process

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from server.settings import config
from camera_process.camera_read import run
from server.models import CamerasModel


class CameraReaderAPI(APIView):
	processes = None

	def get(self, request):
		active = CameraReaderAPI.processes is not None
		return Response(data={"active": active})

	def post(self, request):
		if request.data.get('active') is True and CameraReaderAPI.processes is None:
			CameraReaderAPI.processes = []
			for camera in CamerasModel.objects.filter(active=True):
				process = Process(target=run, args=(camera.id, camera.full_url))
				process.daemon = True
				process.start()
				CameraReaderAPI.processes.append(process)
			return Response(data={"success": True, "details": "The process has been successfully started"})

		if request.data.get('active') is False and self.processes is not None:
			for process in CameraReaderAPI.processes:
				process.terminate()
				CameraReaderAPI.processes = None
			return Response(data={"success": True, "details": "The process has been successfully terminated"})
		return Response(data={"success": False, "details": "The process is already running"})


class ConfigAPI(APIView):

	def get(self, request):
		return Response(config.config)

	def post(self, request):
		try:
			data = config.save(request.data)
		except Exception as e:
			raise ValidationError(e.__str__())
		return Response(data)
