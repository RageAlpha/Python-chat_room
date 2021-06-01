from Server_socket import ServerSocket
from Socket_wrapper import SocketWrapper
import threading
from config import *
from response_protocol import *
from Date_Base import data_base


class SERVER(object):

    def __init__(self):
        """建立socket"""
        self.s_socket = ServerSocket()

        """建立字典来处理是登录还是聊天"""
        self.request_parse = {}
        self.register(REQUEST_LOGIN, self.do_login)
        self.register(REQUEST_CHAT, self.do_chat)

        """建立一个存储登录用户信息的字典"""
        self.client_information = {}

        """建立以数据库链接"""
        self.db = data_base()

    def register(self, request_id, login_chat):
        """使用一个函数来代替建立链接"""
        self.request_parse[request_id] = login_chat

    def start(self):
        """建立服务的收发"""

        while True:
            """与多个客户端建立连接"""
            client_socket, client_addr = self.s_socket.accept()
            new_client_socket = SocketWrapper(client_socket)

            """建立一个线程处理多个客户端的请求"""
            task1_waiting_request = threading.Thread(target=self.waiting_for_request, args=(new_client_socket,))
            task1_waiting_request.start()

    def waiting_for_request(self, new_client_socket):
        """处理客户端的请求"""
        while True:
            """接收客户端的数据"""
            recv_information = new_client_socket.recv_msg()

            if not recv_information:
                """未收到信息时关闭客户端"""
                self.remove_offline_user(new_client_socket)
                new_client_socket.close_socket()
                break

            login_or_chat_date = self.parse_data(recv_information)  # 接收相应的数据
            """处理不同的客户端请求，登录和聊天"""
            request_parse_solve = self.request_parse.get(login_or_chat_date['request_id'])
            if request_parse_solve:
                request_parse_solve(new_client_socket, login_or_chat_date)

            """发送和打印收到的消息"""
            print("You have the data % s" % login_or_chat_date)

    def remove_offline_user(self, new_client_socket):
        """清理离线用户"""
        for username, info in self.client_information.items():
            if info["socket"] == new_client_socket:
                del self.client_information[username]
                break

    def parse_data(self, recv_data):
        """解析客户端发送的数据，并且对不同的请求做对应的操作"""
        """返回相应的解析数据"""

        """
        0001|username|passwd  登录请求
        0002|nickname|message 发送信息请求
        """

        request_list = recv_data.split(DELIMITER)
        request_list_data = {}
        request_list_data['request_id'] = request_list[0]

        if request_list_data['request_id'] == REQUEST_LOGIN:
            request_list_data['username'] = request_list[1]
            request_list_data['passwd'] = request_list[2]

        elif request_list_data['request_id'] == REQUEST_CHAT:
            request_list_data['username'] = request_list[1]
            request_list_data['message'] = request_list[2]

        return request_list_data

    def do_login(self, new_client_socket, request_list_data):
        """处理登录请求"""
        print("Waiting for response")
        username = request_list_data['username']
        passwd = request_list_data['passwd']

        """接收数据库所返回的数据"""
        result, nickname, username = self.check_whether_login(username, passwd)

        """如果登录成功，能够获取到的返回值是结果，昵称，用户名"""
        """存储以及登录成功的用户的socket和昵称"""
        if result == '1':
            self.client_information[username] = {"socket": new_client_socket, "nickname": nickname}
        response_msg = ResponseProtocol.response_login_result(result, nickname, username)
        new_client_socket.send_msg(response_msg)

    def check_whether_login(self, username, passwd):

        # 查询用户是否存在
        query = "select * from users where user_name = '%s' " % username
        query_result = self.db.get_user(query)

        # 不存在用户
        if not query_result:
            return '0', '', username

        # 用户的密码错误
        if passwd != query_result['user_password']:
            return '0', '', username

        # 用户正确登录
        return '1', query_result['user_nickname'], username

    def do_chat(self, new_client_socket, chat_data):
        """处理聊天请求"""
        """拿取数据"""
        print("Waiting for chatting %s" % chat_data)
        username = chat_data['username']
        chat_msg = chat_data['message']
        nickname = self.client_information[username]['nickname']

        """通过rsp来编辑发送给客户端的消息"""
        will_send_msg = ResponseProtocol.response_chat(nickname, chat_msg)

        """对编辑后的信息进行转发"""
        for user_name, info in self.client_information.items():
            if username == user_name:
                continue
            info['socket'].send_msg(will_send_msg)


if __name__ == "__main__":
    SERVER().start()



