from rest_framework import routers

from api.viewsets import CamerasModelViewSet

router = routers.DefaultRouter()

router.register(r'cameras', CamerasModelViewSet, base_name='cameras')
