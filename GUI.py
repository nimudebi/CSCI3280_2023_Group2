from SoundRecorder import *
from RoomList import *

def center_display(w):
    cptr = QDesktopWidget().availableGeometry().center()
    x = cptr.x() - w.width() // 2
    y = cptr.y() - w.height() // 2
    w.move(x, y)


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("./designer/login_icon.png"))
        self.setGeometry(200, 200, 600, 300)

        # username
        self.name_label = QLabel("Username:", self)
        self.name_label.setGeometry(150, 40, 80, 25)  # (x,y,w,h)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Please enter your username")
        self.name_input.setGeometry(150, 70, 300, 25)

        # password
        self.pwd_label = QLabel("Password:", self)
        self.pwd_label.setGeometry(150, 120, 80, 25)
        self.pwd_input = QLineEdit(self)
        self.pwd_input.setPlaceholderText("Please enter your password")
        self.pwd_input.setGeometry(150, 150, 300, 25)
        self.pwd_input.setEchoMode(QLineEdit.Password)

        self.exit_btn = QPushButton("exit", self)
        self.exit_btn.setGeometry(350, 210, 50, 25)
        self.exit_btn.clicked.connect(QApplication.instance().quit)

        self.login_btn = QPushButton("Login", self)
        self.login_btn.setGeometry(180, 210, 50, 25)
        self.login_btn.clicked.connect(self.login)

        center_display(self)

    def login(self):
        username = self.name_input.text()
        password = self.pwd_input.text()
        self.accept()
        '''
        if username and password:
            self.accept()
        else:
            QMessageBox.information(self, "Error!", f"Login Failed! Invalid username or password!")
        '''
    def get_info(self):
        return self.name_input.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))
    login_window = LoginWindow()
    login_window.show()
    if login_window.exec_() == LoginWindow.Accepted:
        username=login_window.get_info()
        w = ChatRoom(username)
        w.show()
    sys.exit(app.exec_())
