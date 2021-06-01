from client_login_window import *
from request_protocol import RequestProtocol
from Client_socket import ClientSocket
from threading import Thread
from client_config import *
from tkinter.messagebox import showinfo
from chat_window import ChatWindow
import sys


class Client(object):

    def __init__(self):
        """初始化登录界面"""
        self.window = LoginWindow()
        self.window.reset_button_click_result(self.remove_username_and_passwd)
        self.window.login_button_click_result(self.send_login_data)
        self.window .close_window(self.leave)

        # 初始化聊天窗口的相关和使用
        self.chatwindow = ChatWindow()
        self.chatwindow.withdraw()
        self.chatwindow.send_button_click(self.send_chat_data)
        self.chatwindow.close_window(self.leave)

        # 客户端链接套接字
        self.client_socket = ClientSocket()

        # 初始化聊天或其他信息的作用
        self.response_solve = {}
        self.response_solve[RESPONSE_LOGIN_RESULT] = self.solve_login
        self.response_solve[RESPONSE_CHAT] = self.solve_chat
        self.register(RESPONSE_LOGIN_RESULT, self.solve_login)
        self.register(REQUEST_CHAT, self.solve_chat)

        # 在线的用户名称
        self.username = None

        # 用户是否在运行程序
        self.is_running = True

    def register(self, request_id, response_solve_function):
        self.response_solve[request_id] = response_solve_function

    def start_window(self):
        """开启登陆界面"""
        self.client_socket.connect()
        # 创建一个接收消息的线程
        Thread(target=self.response_server_msg).start()
        self.window.mainloop()

    def remove_username_and_passwd(self):
        """清除用户和密码"""
        self.window.remove_username()
        self.window.remove_passwd()

    def send_login_data(self):
        """发送登录信息到服务器，接收服务回发的一定信息"""
        username = self.window.get_username()
        passwd = self.window.get_passwd()
        response_data = RequestProtocol.request_login_result(username, passwd)
        print(response_data)
        self.client_socket.send_data(response_data)

    def send_chat_data(self):
        """得到聊天输入框中的内容同时发送到服务器"""
        load_sending_msg = self.chatwindow.get_send_area_msg()  # 获取输入区的信息
        print('a %s a' % load_sending_msg)
        self.chatwindow.remove_send_area_msg()  # 清空输入区的信息

        request_content = RequestProtocol.request_chat(self.username, load_sending_msg)   # 获取信息

        # 将信息发送到服务器
        self.client_socket.send_data(request_content)

        # 显示消息内容到聊天框
        self.chatwindow.add_msg_into_chat_area('I', load_sending_msg)

    def response_server_msg(self):
        """接收服务器发送的消息"""
        while self.is_running:
            recv_data = self.client_socket.recv_data()
            print("You have the message from Server:" + recv_data)
            response_data = self.parse_the_login_or_chat_data(recv_data)


            response_solve_function = self.response_solve[response_data['request_id']]

            if response_solve_function:
                response_solve_function(response_data)


    @staticmethod
    def parse_the_login_or_chat_data(recv_data):
        """
        :param recv_data: 收到的信息 登录信息或者是聊天信息
        1 1001 | 登录成功或者失败 | 昵称 | 用户名
        2 1002 | 请求聊天 | 昵称 | 聊天发送的信息

        :return: 响应的三个结果

        """
        login_or_chat_data = recv_data.split(DELIMITER)
        login_or_chat_data_list = {}
        login_or_chat_data_list['request_id'] = login_or_chat_data[0]

        # 当请求的信息是请求是登录信息时
        if login_or_chat_data_list['request_id'] == RESPONSE_LOGIN_RESULT:
            login_or_chat_data_list['result'] = login_or_chat_data[1]
            login_or_chat_data_list['nickname'] = login_or_chat_data[2]
            login_or_chat_data_list['username'] = login_or_chat_data[3]
        # 当请求的信息是聊天信息时

        elif login_or_chat_data_list['request_id'] == RESPONSE_CHAT:
            login_or_chat_data_list['nickname'] = login_or_chat_data[1]
            login_or_chat_data_list['msg'] = login_or_chat_data[2]

        return login_or_chat_data_list

    def solve_login(self, response_data):
        """处理登录结果"""

        # 登录失败
        result = response_data['result']
        if result == "0":
            showinfo('Tip', "Login Failed,Wrong password or Wrong username")
            print('Wrong password or Wrong username')
            return

        # 登录成功
        showinfo('Tip', 'Successfully Login')
        nickname = response_data['nickname']
        self.username = response_data['username']  # 保存登录用户的名字
        self.chatwindow.title(nickname)

        # 登录成功时显示聊天窗口
        self.chatwindow.update()
        self.chatwindow.deiconify()

        # 隐藏登录窗口
        self.window.withdraw()

    def solve_chat(self, response_data):
        """处理聊天结果"""
        print("you are chatting now", response_data)

        # 处理消息的接收和发送
        send_people = response_data['nickname']
        chat_message = response_data['msg']
        self.chatwindow.add_msg_into_chat_area(send_people, chat_message)

    def leave(self):
        self.is_running = False  # 停止聊天线程
        self.client_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    client = Client()
    client.start_window()
