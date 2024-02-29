import sys
import os
import threading
import time
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer, QUrl, Qt
import qtawesome as qta

from version import *
from speech_to_text import speech_to_text


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

    @staticmethod
    def open_next_window():
        w = SoundRecorder()
        w.show()


def count_files(path):
    file_list = os.listdir(path)  # 获取文件夹中所有文件的列表
    num_files = len(file_list)  # 获取文件个数
    return num_files, file_list


class SoundRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.showMinimized)
        self.ui.pushButton.clicked.connect(self.close)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.pushButton_11.clicked.connect(self.load_audio)
        self.ui.listWidget.itemClicked.connect(self.audio_selected)
        self.ui.listWidget.itemDoubleClicked.connect(self.audio_play)

        self.ui.listWidget.setContextMenuPolicy(3)
        self.ui.listWidget.customContextMenuRequested.connect(self.show_menu)

        self.timing = QTimer()
        self.filepath = None
        self.filename = None
        self.sound_player = QMediaPlayer()
        self.sound_player.setVolume(66)

        self.sound_player.positionChanged.connect(self.update_play_slider)
        self.sound_player.mediaStatusChanged.connect(self.final)
        self.ui.horizontalSlider.sliderMoved.connect(self.playing_adjusting)
        self.ui.horizontalSlider.sliderReleased.connect(self.playing_adjusted)

        # attributes of speech-to-text window
        self.speech_to_text_window = None

        self.playing = False
        self.pre_music_index = 0  # 上一首歌的index
        self.ui.pushButton_5.clicked.connect(self.play_change)

        # Todo 连到录音函数中
        self.recording = True
        self.ui.pushButton_9.clicked.connect(self.record_change)

        # Todo 如何实现弹出一个音量条
        # self.ui.pushButton_8.clicked.connect(self.volume_adjust)
        # self.volume_line.valueChanged.connect(self.volume_adjust)  # 拖动音量条改变音量

    def show_menu(self, pos):
        context_menu = QMenu(self)
        trim_action = QAction("Audio Trim", self)
        # TODO：添加trim函数
        # trim_action.triggered.connect(self.)
        # context_menu.addAction(trim_action)
        s2t_action = QAction("Speech to Text", self)
        s2t_action.triggered.connect(self.open_speech_to_text_window)
        context_menu.addAction(s2t_action)

        context_menu.exec_(self.ui.listWidget.mapToGlobal(pos))

    def update_play_slider(self, position):
        duration = self.sound_player.duration()
        self.ui.horizontalSlider.setRange(0, duration)
        self.ui.horizontalSlider.setValue(position)

    def playing_adjusting(self, position):
        self.sound_player.pause()
        self.sound_player.setPosition(position)

    def playing_adjusted(self):
        if self.playing:
            self.sound_player.play()

    def final(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_change()

    def load_audio(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio Files (*.wav)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            for filename in filenames:
                self.ui.listWidget.addItem(os.path.basename(filename))

    def audio_selected(self, item):
        self.filename = item.text()
        self.filepath = os.path.join(os.getcwd(), self.filename)
        media_content = QMediaContent(QUrl.fromLocalFile(self.filepath))

    def audio_play(self, item):
        filename = item.text()
        filepath = os.path.join(os.getcwd(), filename)
        media_content = QMediaContent(QUrl.fromLocalFile(filepath))
        self.sound_player.setMedia(media_content)
        self.playing = True
        self.sound_player.play()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designer/circle-pause-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_5.setIcon(icon)

    def play_change(self):

        if self.playing:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("designer/circle-play-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_5.setIcon(icon)
            self.sound_player.pause()
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("designer/circle-pause-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_5.setIcon(icon)
            self.sound_player.play()
        self.playing = not self.playing

    def record_change(self):
        if self.recording:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("designer/circle-stop-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_9.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("designer/record-vinyl-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_9.setIcon(icon)
        self.recording = not self.recording

    # Todo 弹出窗口 to be implemented
    def volume_adjust(self):
        self.sound_player.setVolume(self.volume_line.value())
        if self.volume_line.value() == 0:
            self.volume.setPixmap(QPixmap("./designer/volume-xmark-solid.svg"))
        elif self.volume_line.value() < 50:
            self.volume.setPixmap(QPixmap("./designer/volume-low-solid.svg"))
        elif self.volume_line.value() <= 100:
            self.volume.setPixmap(QPixmap("./designer/volume-high-solid.svg"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.isMaximized() == False:
            if -200 <= event.y() <= 200:
                self.m_flag = True
                self.m_Position = event.globalPos() - self.pos()
                event.accept()

    def mouseMoveEvent(self, mouse_event):
        if Qt.LeftButton and self.m_flag:
            if -200 <= mouse_event.y() <= 200:
                self.move(mouse_event.globalPos() - self.m_Position)
                mouse_event.accept()

    # added by yitian
    # temporarily add this function here
    def audio_clicked_to_text(self, item):
        # filename = item.text()
        # filepath = os.path.join(os.getcwd(), filename)
        self.open_speech_to_text_window()

    # open a new speech-to-text window
    def open_speech_to_text_window(self):
        if self.speech_to_text_window is None:
            self.speech_to_text_window = QWidget()
            self.speech_to_text_window.transcript = ""

            # selected file name
            selected_file_name = QLineEdit(self.speech_to_text_window)
            selected_file_name.setGeometry(50, 30, 370, 30)
            selected_file_name.setReadOnly(True)
            selected_file_name.setObjectName("selected_file_name")
            selected_file_name.setText(self.filename)

            # start transcribing button
            transcribe_button = QPushButton(self.speech_to_text_window)
            transcribe_button.setText("Transcribe")
            transcribe_button.setGeometry(450, 30, 100, 30)
            transcribe_button.clicked.connect(self.start_transcription)

            # transcript area
            transcript_area = QTextEdit(self.speech_to_text_window)
            transcript_area.setObjectName("transcript_area")
            transcript_area.setGeometry(50, 80, 500, 290)
            transcript_area.setReadOnly(True)
            transcript_area.setText(self.speech_to_text_window.transcript)

            self.speech_to_text_window.setGeometry(100, 100, 600, 400)
            self.speech_to_text_window.setWindowTitle("Speech to text")
            self.speech_to_text_window.show()
        else:
            self.speech_to_text_window.transcript = ""
            selected_file_name = self.speech_to_text_window.findChild(QLineEdit, "selected_file_name")
            selected_file_name.setText(self.filename)
            transcript_area = self.speech_to_text_window.findChild(QTextEdit, "transcript_area")
            transcript_area.setText("")
            self.speech_to_text_window.show()

    def start_transcription(self):
        transcript_area = self.speech_to_text_window.findChild(QTextEdit, "transcript_area")
        try:
            transcript = speech_to_text(self.filepath)
            transcript_area.setText(transcript)
        except Exception as e:
            transcript_area.setText("Error occurred during transcription: " + str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))
    login_window = LoginWindow()
    login_window.show()
    if login_window.exec_() == LoginWindow.Accepted:
        w = SoundRecorder()
        w.show()
    sys.exit(app.exec_())

'''
import sys
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, \
    QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QImage, QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot_audio(self, audio_data):
        self.ax.clear()
        self.ax.plot(audio_data)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())


class ControlPanel(QWidget):
    def __init__(self, title):
        super().__init__()

        #TODO  这里有问题，如何和RecordingExplorer联动，找到目前选择了哪个文件
        self.sound = QSound('sound.wav')
        self.sound.setLoops(1)


        record_btn = QPushButton()
        record_btn.setsetIcon(qta.icon("ph.record-bold"))
        record_btn.setStyleSheet("background-color: white; color: red;")
        record_btn.setFixedSize(50, 50)
        self.button.clicked.connect(self.record_change)
        self.record_flag = True

        play_btn = QPushButton()
        play_btn.setsetIcon(qta.icon("fa.play-circle-o"))
        play_btn.setFixedSize(50, 50)
        play_btn.setStyleSheet("background-color: white; color: black;")
        self.button.clicked.connect(self.play_change)
        self.play_flag = True
    def record_change(self):
        if self.record_flag:
            self.setsetIcon(qta.icon("fa5.stop-circle"))
            self.setStyleSheet("background-color: white; color: red;")
            self.setFixedSize(50, 50)

        else:
            self.setsetIcon(qta.icon("ph.record-bold"))
            self.setStyleSheet("background-color: white; color: red;")
            self.setFixedSize(50, 50)

        self.record_flag = not self.record_flag
    def play_change(self):
        if self.play_flag:
            self.setsetIcon(qta.icon("fa.play-circle-o"))
            self.setStyleSheet("background-color: white; color: black;")
            self.setFixedSize(50, 50)
            self.sound.play
        else:
            self.setsetIcon(qta.icon("fa5.pause-circle"))
            self.setStyleSheet("background-color: white; color: black;")
            self.setFixedSize(50, 50)

        self.play_flag = not self.play_flag


class RecordingExplorer(QMainWindow):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"This is {title}"))
        layout.addWidget(QPushButton("Button"))
        self.setLayout(layout)


class SoundWindow(QWidget):
    def __init__(self,path):
        super(SoundWindow, self).__init__()
        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setSource(QUrl.fromLocalFile(path))
        self.sound_effect.setVolume(1.0)
        def create_stacked_layout():
            self.stacked_layout = QStackedLayout()


            path=".//sound_files"
            num_files, file_list=count_files(path)

            for i in range(num):
                x
                self.stacked_layout.addWidget(x)

        # Recording Explorer
        self.RE = QWidget()
        self.RE.setObjectName('Recording Explorer')
        self.RE_layout = QGridLayout()
        self.RE.setLayout(self.RE_layout)

        self.setWindowTitle("Sound Recorder")
        self.setGeometry(100, 100, 1500, 800)
        self.create_stacked_layout()
        container=QVBoxLayout()
        re = RecordingExplorer("Recording Explorer")
        cp = ControlPanel("Control Panel")
        w=QWidget()
        w.setLayout(self.stacked_layout)
        re = RecordingExplorer("Recording Explorer")

        top_right_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        center_display(self)
'''

'''

import os
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PyQt5.QtGui import QPixmap

class FileViewer(QWidget):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Viewer')

        # 创建主水平布局
        mainLayout = QHBoxLayout()

        # 创建左侧垂直布局
        leftLayout = QVBoxLayout()

        # 创建滚动区域
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        # 创建滚动区域内的 widget
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)

        # 创建按钮列表
        self.buttons = []

        # 遍历目录中的文件
        for file in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, file)):
                # 创建按钮并添加到布局
                button = QPushButton(file)
                button.clicked.connect(lambda state, file=file: self.showImage(file))
                scrollLayout.addWidget(button)
                self.buttons.append(button)

        scrollArea.setWidget(scrollWidget)
        leftLayout.addWidget(scrollArea)

        # 创建右侧标签用于显示图片
        self.imageLabel = QLabel()
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.imageLabel)

        # 将左侧和右侧布局添加到主布局中
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)

    def showImage(self, filename):
        # 获取文件路径
        filepath = os.path.join(self.directory, filename)
        # 显示图片
        pixmap = QPixmap(filepath)
        self.imageLabel.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication([])
    directory = './sound_files'
    fileViewer = FileViewer(directory)
    fileViewer.show()
    app.exec_()



def playVideo(self, filename):
        # 获取文件路径
        filepath = os.path.join(self.directory, filename)
        # 加载视频
        self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
        # 播放视频
        self.videoPlayer.play()





class qt_view(QWidget):
    def __init__(self):
        super(qt_view, self).__init__()

        self.resize(600, 250)
        self.setWindowTitle("圆点选择")

        self.radioButton_1 = QtWidgets.QRadioButton(self)
        self.radioButton_1.setGeometry(QtCore.QRect(230, 100, 89, 16))
        self.radioButton_1.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(310, 100, 89, 16))
        self.radioButton_2.setStyleSheet("font-family:微软雅黑; color:black;")
        self.radioButton_2.setObjectName("radioButton_2")

        translate = QtCore.QCoreApplication.translate
        self.radioButton_1.setText(translate("Form", "选项1"))
        self.radioButton_2.setText(translate("Form", "选项2"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my = qt_view()
    my.show()







        handle_rect = self.style().subControlRect(QStyle.CC_Slider, self, QStyle.SC_SliderHandle)
            if handle_rect.contains(event.pos()):
                # 如果鼠标在滑块上，设置鼠标指针为选中手势
                QApplication.setOverrideCursor(Qt.PointingHandCursor)
            else:
                # 否则恢复默认的鼠标指针样式
                QApplication.restoreOverrideCursor()
'''
