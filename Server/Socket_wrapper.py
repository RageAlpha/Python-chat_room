class SocketWrapper(object):

    def __init__(self, tcp_socket):
        self.tcp_socket = tcp_socket

    def recv_msg(self):
        """接收数据"""
        try:
            return self.tcp_socket.recv(1024).decode("utf-8")
        except:
            return ""

    def send_msg(self, msg):
        """发送数据"""

        return self.tcp_socket.send(msg.encode("utf-8"))

    def close_socket(self):
        self.tcp_socket.close()
