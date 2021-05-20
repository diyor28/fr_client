from django.conf.urls import url
from django.urls import path

from api.apiviews import ConfigAPI, CameraReaderAPI

urlpatterns = [
	path('config/', ConfigAPI.as_view(), name="config"),
	path('camera_reader/', CameraReaderAPI.as_view(), name="camera_reader")
]
