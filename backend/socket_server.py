import socket
import json


class Server:
	def __init__(self, host, port, header_size, buffer_size=1024):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((host, port))
		self.server.listen(5)
		self.header_size = header_size
		self.buffer_size = buffer_size

	def run(self):
		while True:
			print(self.receive())

	def receive(self):
		client_socket, address = self.server.accept()
		print(f"Accepted connection from {address}")
		message = client_socket.recv(self.buffer_size)
		if len(message) > 0:
			message = message.decode('utf-8')
			message_length, message = int(message[:self.header_size]), message[self.header_size:]
			if message_length < self.buffer_size:
				client_socket.close()
				return json.loads(message)
			return message + self.receive()


server = Server('localhost', 9000, 10)
server.run()
