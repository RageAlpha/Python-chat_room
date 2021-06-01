from socket import *
from config import *


class ServerSocket(socket):
    """建立服务器的基本套接字"""

    def __init__(self):
        super(ServerSocket, self).__init__(AF_INET, SOCK_STREAM)
        self.bind((SERVER_IP, SERVER_PORT))
        self.listen(128)
