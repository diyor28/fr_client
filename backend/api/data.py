from api.connection import VectorsAPI, TasksAPI, UserAPI

SUCCESS_CODE = (200, 201, 202, 203)


class BaseWrapper:
	class Object:
		pass

	api_caller = None

	@classmethod
	def create_instance(cls, data):
		instance = cls.Object()
		for key, value in data.items():
			instance.__setattr__(key, value)
		return instance

	@classmethod
	def retrieve(cls, pk=None, params=None):
		response = cls.api_caller.get(pk=pk, params=params)
		if response.status_code in SUCCESS_CODE:
			if pk:
				return cls.create_instance(data=response.json())
			users = []
			for element in response.json():
				instance = cls.create_instance(data=element)
				users.append(instance)

	@classmethod
	def create(cls, fields, files):
		response = cls.api_caller.post(data=fields, files=files)
		if response.status_code in SUCCESS_CODE:
			return cls.create_instance(data=response.json())

	@classmethod
	def delete(cls, pk):
		response = cls.api_caller.delete(pk)
		if response.status_code in SUCCESS_CODE:
			return response.status_code

	@classmethod
	def update(cls, pk, fields):
		response = cls.api_caller.patch(pk, data=fields)
		if response.status_code in SUCCESS_CODE:
			return cls.create_instance(data=response.json())


class UsersWrapper(BaseWrapper):
	api_caller = UserAPI


class TasksWrapper(BaseWrapper):
	api_caller = TasksAPI


class VectorsWrapper(BaseWrapper):
	api_caller = VectorsAPI
