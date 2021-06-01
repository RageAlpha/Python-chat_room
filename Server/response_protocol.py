from config import *


class ResponseProtocol(object):
    """服务器的字符串响应"""

    @staticmethod
    # 登录时候的函数
    def response_login_result(result, nickname, username):

        """
        :param result: 如果result的值为1，表示登录成功；如果值为0，表示登录失败
        :param nickname: 登录时的nickname
        :param username: 登录时候的账户
        :return: return 用户登录的结果
        """

        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    # 聊天时候的函数
    def response_chat(nickname, messages):
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])
