import socket
import json


class Client:
	def __init__(self, host, port, header_size):
		self.header_size = header_size
		self.host = host
		self.port = port
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.host, self.port))

	def send(self, message):
		message = json.dumps(message)
		message = f"{len(message):<{self.header_size}}" + message
		self.connection.send(bytes(message, 'utf-8'))

	def close(self):
		self.connection.close()


client = Client('localhost', 9000, 10)
client.send('hello world')
