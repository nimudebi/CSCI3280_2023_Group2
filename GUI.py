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
from audio_change_start_end import audio_change_start_end as cut


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
        self.m_flag=False
        self.timing = QTimer()
        self.filepath = None
        self.filename = None
        self.sound_player = QMediaPlayer()

        self.sound_selected_filepath = None
        self.sound_selected_filename = None
        self.sound_selected = QMediaPlayer()

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

        self.sound_player.setVolume(66)
        self.ui.horizontalSlider_2.setValue(self.ui.horizontalSlider_2.maximum())
        self.ui.horizontalSlider.setDisabled(True)
        self.ui.horizontalSlider_2.setDisabled(True)
        self.ui.horizontalSlider_3.setDisabled(True)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        self.sound_player.positionChanged.connect(self.update_play_slider)
        self.sound_player.mediaStatusChanged.connect(self.final)
        self.ui.horizontalSlider.sliderMoved.connect(self.playing_adjusting)
        self.ui.horizontalSlider.sliderReleased.connect(self.playing_adjusted)

        # cut the audio
        self.ui.pushButton_2.clicked.connect(self.cut_audio)

        # attributes of speech-to-text window
        self.speech_to_text_window = None
        self.audio_cropping_window = None

        self.playing = False
        self.pre_music_index = 0  # 上一首歌的index
        self.ui.pushButton_5.clicked.connect(self.play_change)


        # Todo 连到录音函数中
        self.recording = True
        self.ui.pushButton_9.clicked.connect(self.record_change)

        # Todo 如何实现弹出一个音量条
        # self.ui.pushButton_8.clicked.connect(self.volume_adjust)
        # self.volume_line.valueChanged.connect(self.volume_adjust)  # 拖动音量条改变音量

    def cut_audio(self):
        start_time=self.ui.horizontalSlider_3.value()//1000
        end_time=self.ui.horizontalSlider_2.value()//1000
        if(start_time>=end_time):
            QMessageBox.critical(self, "Error", f"An error occurred: start time should less than end time")
            return
        header,audio_data_new=cut(self.sound_selected_filepath, start_time, end_time)
        save_path, _ = QFileDialog.getSaveFileName(self, "保存剪切后的音频", "", "WAV 文件 (*.wav)")
        if save_path:
            with open(save_path, 'wb') as wav_out:
                wav_out.write(header)
                wav_out.write(audio_data_new)

    def show_menu(self, pos):
        item = self.ui.listWidget.itemAt(pos)
        if item is not None:
            if item.isSelected():
                self.sound_selected_filename = item.text()
                self.sound_selected_filepath = os.path.join(os.getcwd(), self.sound_selected_filename)


            context_menu = QMenu(self)
            trim_action = QAction("Audio Trim", self)
            # TODO：添加trim函数
            # trim_action.triggered.connect(self.)
            # context_menu.addAction(trim_action)
            s2t_action = QAction("Speech to Text", self)
            s2t_action.triggered.connect(self.open_speech_to_text_window)
            context_menu.addAction(s2t_action)
            context_menu.setStyleSheet("""
                QMenu {
                    background-color: rgb(251, 255, 233);
                    border: 1px solid #CCCCCC;
                }
                QMenu::item {
                    padding: 6px 20px;
                }
                QMenu::item:selected {
                    background-color: rgba(255, 217, 1,30);
                    color: rgba(0, 0, 0);
                }
            """)

            context_menu.exec_(self.ui.listWidget.mapToGlobal(pos))

    def update_play_slider(self, position):
        duration = self.sound_player.duration()
        self.ui.horizontalSlider.setRange(0, duration)
        self.ui.horizontalSlider.setValue(position)
        self.ui.horizontalSlider.setDisabled(False)
        self.ui.horizontalSlider_2.setDisabled(False)
        self.ui.horizontalSlider_3.setDisabled(False)
        self.ui.horizontalSlider_2.setRange(0, self.sound_selected.duration())
        self.ui.horizontalSlider_3.setRange(0, self.sound_selected.duration())
        self.ui.horizontalSlider_2.setValue(self.sound_selected.duration())
        self.ui.horizontalSlider_3.setValue(0)


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
        self.sound_selected_filename = item.text()
        self.sound_selected_filepath = os.path.join(os.getcwd(), self.sound_selected_filename)
        m = QMediaContent(QUrl.fromLocalFile(self.sound_selected_filepath))
        self.sound_selected.setMedia(m)


    def audio_play(self, item):
        self.filename = item.text()
        self.filepath = os.path.join(os.getcwd(), self.filename)
        media_content = QMediaContent(QUrl.fromLocalFile(self.filepath))
        self.sound_player.setMedia(media_content)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)
        self.playing = True
        self.sound_player.play()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./designer/circle-pause-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_5.setIcon(icon)

    def play_change(self):

        if self.playing:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/circle-play-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_5.setIcon(icon)
            self.sound_player.pause()
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/circle-pause-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_5.setIcon(icon)
            self.sound_player.play()
        self.playing = not self.playing

    def record_change(self):
        if self.recording:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/circle-stop-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_9.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/record-vinyl-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

    def start_transcription(self):
        transcript_area = self.speech_to_text_window.findChild(QTextEdit, "transcript_area")
        try:
            transcript = speech_to_text(self.sound_selected_filepath)
            transcript_area.setText(transcript)
        except Exception as e:
            transcript_area.setText("Error occurred during transcription: " + str(e))

    def open_speech_to_text_window(self):
        if self.speech_to_text_window is None:
            self.speech_to_text_window = QWidget()
            self.speech_to_text_window.transcript = ""
            # selected file name
            selected_file_name = QLineEdit(self.speech_to_text_window)
            selected_file_name.setGeometry(50, 30, 250, 30)
            selected_file_name.setReadOnly(True)
            selected_file_name.setObjectName("selected_file_name")
            selected_file_name.setText(self.sound_selected_filename)

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
            selected_file_name.setText(self.sound_selected_filename)
            transcript_area = self.speech_to_text_window.findChild(QTextEdit, "transcript_area")
            transcript_area.setText("")
            self.speech_to_text_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))
    login_window = LoginWindow()
    login_window.show()
    if login_window.exec_() == LoginWindow.Accepted:
        w = SoundRecorder()
        w.show()
    sys.exit(app.exec_())
