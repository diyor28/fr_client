from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from api.serializers import CamerasModelSerializer
from server.models import CamerasModel


class CsrfExemptSessionAuthentication(SessionAuthentication):
	def enforce_csrf(self, request):
		return


class CamerasModelViewSet(viewsets.ModelViewSet):
	serializer_class = CamerasModelSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

	def get_queryset(self):
		queryset = CamerasModel.objects.all()
		return queryset
