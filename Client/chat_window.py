from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Button
from tkinter import Text
from tkinter import END
from time import time, strftime, localtime
from tkinter import UNITS

class ChatWindow(Toplevel):

    def __init__(self):
        super(ChatWindow, self).__init__()

        self.geometry('%dx%d' % (620, 400))
        self.resizable(False, False)
        self.add_widget()
        self.send_button_click(lambda: self.add_msg_into_chat_area())

    def add_widget(self):
        # 聊天区域
        chat_area = ScrolledText(self)
        chat_area['width'] = 85
        chat_area['height'] = 20
        chat_area.grid(row=0, column=0, columnspan=2)

        # 标明发送信息的用户
        # 标明发送信息的用户颜色为绿色
        chat_area.tag_config('LightSlateGray', foreground='#778899')
        chat_area.tag_config('system', foreground='red')
        self.children['chat_area'] = chat_area
        # 输入信息区域
        send_area = Text(self, name='send_msg_area')
        send_area['width'] = 75
        send_area['height'] = 7
        send_area.grid(row=1, column=0, pady=10)


        # 发送按钮
        send_button = Button(self, name="send_msg_button")
        send_button['text'] = 'Enter'
        send_button['width'] = 5
        send_button['height'] = 2
        send_button.grid(row=1, column=1)

    def chat_window_title(self, title):
        # 显示聊天窗口的标题
        self.title('Welcome % s come to the chat room' % title)

        # 实现发送按钮的功能
    def send_button_click(self, command):
        self.children['send_msg_button']['command'] = command

        # 获取发送的信息
    def get_send_area_msg(self):
        return self.children['send_msg_area'].get(0.0, END)

        # 清空聊天的信息
    def remove_send_area_msg(self):
        self.children['send_msg_area'].delete(0.0, END)

    def add_msg_into_chat_area(self,user_nickname, message):
        # 加入发送者的信息和时间
        # 加入发送的信息，换行来方便识别
        send_time = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        send_information = '%s : %s\n' % (user_nickname, send_time)
        self.children['chat_area'].insert(END, send_information, 'LightSlateGray')
        self.children['chat_area'].insert(END, message + '\n')

        self.children['chat_area'].yview_scroll(3, UNITS)

    def close_window(self,command):
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == "__main__":
   ChatWindow().mainloop()
