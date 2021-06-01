from socket import *
from client_config import *


class ClientSocket(socket):

    def __init__(self):
        super(ClientSocket, self).__init__(AF_INET, SOCK_STREAM)

    def connect(self):
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        return self.recv(1024).decode('utf-8')

    def send_data(self, msg):
        return self.send(msg.encode('utf-8'))

