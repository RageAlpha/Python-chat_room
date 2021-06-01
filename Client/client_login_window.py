from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Frame
from tkinter import Entry
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import END


class LoginWindow(Tk):
    """初始化登录窗口"""
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.window_initialize()
        self.add_window_widget()


    """设置窗口"""
    def window_initialize(self):
        # 登录的窗口标题
        self.title("YYGQ")

        # 设置窗口不能拉伸
        self.resizable(False, False)

        # 登录的窗口大小
        window_width = 200
        window_height = 280

        screen_size_height = self.winfo_screenwidth()
        screen_size_width = self.winfo_screenheight()

        pos_x = (screen_size_height - window_height) / 2
        pos_y = (screen_size_width - window_width) / 2

        self.geometry('%dx%d+%d+%d' % (window_height, window_width, pos_x, pos_y))

    """增加控件"""
    def add_window_widget(self):

        # 用户名的标签
        username_label = Label(self)
        username_label['text'] = 'Username:'
        username_label.grid(row=5, column=0, padx=25, pady=10)

        # 用户名标签的文本
        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 12
        username_entry.grid(row=5, column=1)

        # 密码的标签
        password_label = Label(self)
        password_label['text'] = 'Password:'
        password_label.grid(row=6, column=0, padx=25, pady=0)

        # 密码标签对应的文本
        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 12
        password_entry.grid(row=6, column=1)

        # 按钮
        button_frame = Frame(self, name='button_frame')

        # 登录按钮的建立
        login_button = Button(button_frame, name="login_button")
        login_button['text'] = ' Login '
        login_button.pack(side=LEFT, padx=30)

        # 重置按钮的建立
        reset_button = Button(button_frame, name="reset_button")
        reset_button['text'] = ' Reset '
        reset_button.pack(side=RIGHT)

        # 框架的组成打大小和位置
        button_frame.grid(row=9, columnspan=7)

    def remove_username(self):
        """删除用户名"""
        self.children['username_entry'].delete(0, END)

    def remove_passwd(self):
        """删除密码"""
        self.children['password_entry'].delete(0, END)

    def get_username(self):
        """获取用户名"""
        return self.children['username_entry'].get()

    def get_passwd(self):
        """得到密码"""
        return self.children['password_entry'].get()

    def login_button_click_result(self, command):
        # 登录按钮的响应结果 ，执行command命令操作
        login_button_click = self.children['button_frame'].children['login_button']
        login_button_click['command'] = command

        # 重置按钮的响应结果， 执行command命令操作
    def reset_button_click_result(self, command):
        reset_button_click = self.children['button_frame'].children['reset_button']
        reset_button_click['command'] = command

    def close_window(self,command):
        """关闭登录窗口"""
        self.protocol('WM_DELETE_WINDOW', command)


if __name__ == "__main__":
    window_start = LoginWindow()
    window_start.mainloop()