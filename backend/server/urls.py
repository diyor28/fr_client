from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from api.routers import router
from server.views import StreamsView

urlpatterns = [
	path('api/', include(router.urls)),
	path('api/', include(('api.urls', 'api'), namespace='api')),
	url(r'^streams/(?P<pk>\d+)/$', StreamsView.as_view(), name='streams')
]
