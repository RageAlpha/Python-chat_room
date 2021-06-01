from client_config import *


class RequestProtocol(object):
    """请求登录的结果"""
    @staticmethod
    def request_login_result(username, password):
        """
        
        :param username: 用户的名字
        :param password: 用户的密码
        :return: 
        """
    
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    """请求聊天的信息"""
    @staticmethod
    def request_chat(username, message):
        return DELIMITER.join([REQUEST_CHAT, username, message])





