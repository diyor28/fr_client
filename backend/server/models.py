from django.db import models


class CamerasModel(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	ip = models.GenericIPAddressField(blank=True, null=True)
	channel = models.IntegerField(blank=True, null=True)
	port = models.IntegerField(blank=True, null=True)
	active = models.BooleanField(blank=True, null=True)
	login = models.CharField(max_length=40, blank=True, null=True)
	password = models.CharField(max_length=40, blank=True, null=True)
	full_url = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		db_table = 'cameras'
