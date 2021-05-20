from rest_framework import serializers

from server.models import CamerasModel
from ml.utils import construct_camera_url


class CamerasModelSerializer(serializers.ModelSerializer):
	def to_internal_value(self, data):
		if data.get("full_url") is None:
			data['full_url'] = construct_camera_url(data.get("ip"),
													data.get("port"),
													data.get("login"),
													data.get("password"))
		return data

	class Meta:
		model = CamerasModel
		fields = '__all__'


class ConfigSerializer(serializers.Serializer):

	pass
