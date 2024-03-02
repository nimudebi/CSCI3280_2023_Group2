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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from audio_change_start_end import audio_change_start_end as cut
import pyaudio
from write_wav_file import write_wav_file
from playback_and_speed_control import speed_control
from audio_visualization_fixed import audio_visualization_fixed
from tone_editing import tone_editing


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
        self.m_flag = False
        self.timing = QTimer()
        self.filepath = None
        self.filename = None
        self.sound_player = QMediaPlayer()

        self.speed = 1
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

        self.editing_window=None

        # Added by Yitian
        # Switch to the previous and next audio file buttons
        self.ui.pushButton_6.clicked.connect(self.switch_to_previous_audio)
        self.ui.pushButton_4.clicked.connect(self.switch_to_next_audio)
        self.ui.pushButton_6.setDisabled(True)
        self.ui.pushButton_4.setDisabled(True)
        self.flag_any_audio_file_selected = False

        self.sound_player.positionChanged.connect(self.update_play_slider)
        self.sound_player.mediaStatusChanged.connect(self.final)
        self.ui.horizontalSlider.sliderMoved.connect(self.playing_adjusting)
        self.ui.horizontalSlider.sliderReleased.connect(self.playing_adjusted)
        self.ui.horizontalSlider_3.setTickInterval(1000)
        self.ui.horizontalSlider_2.setTickInterval(1000)
        # cut the audio
        self.ui.pushButton_2.clicked.connect(self.cut_audio)
        self.final_flag = False

        # Added by Yitian
        # attributes of speech-to-text window
        self.speech_to_text_window = None
        self.audio_cropping_window = None
        self.change_label = False
        self.playing = False
        self.pre_music_index = 0
        self.ui.pushButton_5.clicked.connect(self.play_change)

        self.recording = False
        self.ui.pushButton_9.clicked.connect(self.record_change)

        self.menu = QMenu()
        self.action1 = QAction("x0.5")
        self.action1.triggered.connect(self.speed1)
        self.menu.addAction(self.action1)
        self.action2 = QAction("x1.0")
        self.action2.triggered.connect(self.speed2)
        self.menu.addAction(self.action2)
        self.action3 = QAction("x2.0")
        self.action3.triggered.connect(self.speed3)
        self.menu.addAction(self.action3)

        self.ui.toolButton.setMenu(self.menu)
        self.ui.toolButton.setPopupMode(QToolButton.InstantPopup)

    def speed1(self):
        if self.filepath:
            self.speed = 0.5
            speed_control(self.filepath, 0.5)

    def speed2(self):
        self.speed = 1
        return

    def speed3(self):
        if self.filepath:
            self.speed = 2
            speed_control(self.filepath, 2)

        # To be implement
        # self.ui.pushButton_8.clicked.connect(self.volume_adjust)
        # self.volume_line.valueChanged.connect(self.volume_adjust)

    def overwrite(self):
        start_time = self.ui.horizontalSlider_3.value() // 1000

    def cut_audio(self):
        start_time = self.ui.horizontalSlider_3.value() // 1000
        end_time = self.ui.horizontalSlider_2.value() // 1000
        if (start_time >= end_time):
            QMessageBox.critical(self, "Error", f"An error occurred: start time should less than end time")
            return
        header, audio_data_new = cut(self.sound_selected_filepath, start_time, end_time)
        save_path, _ = QFileDialog.getSaveFileName(self, "Save as..?", "", "WAV FILE (*.wav)")
        if save_path:
            with open(save_path, 'wb') as wav_out:
                wav_out.write(header)
                wav_out.write(audio_data_new)

    def show_menu(self, pos):
        item = self.ui.listWidget.itemAt(pos)
        if item is not None:
            if item.isSelected():
                self.sound_selected_filename = item.text()
                self.sound_selected_filepath = item.data(Qt.UserRole)

            context_menu = QMenu(self)
            tone_changing_action = QAction("Tone Changing", self)
            tone_changing_action.triggered.connect(self.open_editing_window)
            context_menu.addAction(tone_changing_action)

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
        if self.change_label is not True:
            self.change_label = True
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
            self.final_flag = True

    def load_audio(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio Files (*.wav)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            for filename in filenames:
                item = QListWidgetItem(os.path.basename(filename))
                item.setData(Qt.UserRole, filename)
                self.ui.listWidget.addItem(item)

    def visualization(self):
        audio_image = audio_visualization_fixed(self.sound_selected_filepath)
        # 将图像数据转换为QImage对象
        height, width, channel = audio_image.shape
        bytes_per_line = channel * width
        qimage = QImage(audio_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # 设置QLabel的图像
        self.ui.label_2.setPixmap(pixmap)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.setAlignment(Qt.AlignCenter)

        # 设置QLabel的aspectRatioMode属性为保持比例缩放
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.setPixmap(pixmap.scaled(self.ui.label_2.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def audio_selected(self, item):
        self.change_label = False
        self.sound_selected_filename = item.text()
        self.sound_selected_filepath = item.data(Qt.UserRole)
        m = QMediaContent(QUrl.fromLocalFile(self.sound_selected_filepath))
        self.sound_selected.setMedia(m)
        self.visualization()

        if not self.flag_any_audio_file_selected:
            self.ui.pushButton_6.setDisabled(False)
            self.ui.pushButton_4.setDisabled(False)
            self.flag_any_audio_file_selected = True

    def audio_play(self, item):
        self.filename = item.text()
        self.filepath = item.data(Qt.UserRole)
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
        if self.final_flag:
            self.final_flag = False
            if self.speed != 1:
                filename = f"{self.filename}_{self.speed}.wav"
                self.filepath = os.path.join(os.getcwd(), filename)
                media_content = QMediaContent(QUrl.fromLocalFile(self.filepath))
                self.sound_player.setMedia(media_content)

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
        self.recording = not self.recording
        if self.recording:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/circle-stop-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_9.setIcon(icon)
            self.stream = self.open_stream()
            self.frames = []
            self.stream.start_stream()
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("./designer/record-vinyl-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_9.setIcon(icon)
            self.stop_recording()

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.save_recording()

    def open_stream(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=4 * 1024,
                            stream_callback=self.callback)
        return stream

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

    def save_recording(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save as..?", "", "WAV FILE (*.wav)")
        if save_path:
            audio = pyaudio.PyAudio()
            write_wav_file(save_path, b''.join(self.frames))

    # Added by Yitian
    # Switch to the previous and next audio file
    def switch_to_previous_audio(self):
        current_row = self.ui.listWidget.currentRow()
        previous_row = (current_row - 1) % self.ui.listWidget.count()
        # If there is only 1 item in the list, previous_item will be the current item
        # If current_item is the first in the list, previous_item will be the last item
        previous_item = self.ui.listWidget.item(previous_row)
        self.ui.listWidget.setCurrentItem(previous_item)
        self.audio_selected(previous_item)
        self.audio_play(previous_item)

    def switch_to_next_audio(self):
        current_row = self.ui.listWidget.currentRow()
        next_row = (current_row + 1) % self.ui.listWidget.count()
        # If there is only 1 item in the list, next_item will be the current item
        # If current_item is the last in the list, next_item will be the first item
        next_item = self.ui.listWidget.item(next_row)
        self.ui.listWidget.setCurrentItem(next_item)
        self.audio_selected(next_item)
        self.audio_play(next_item)

    # to be implemented
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

    def open_editing_window(self):
        if self.editing_window is None:
            self.editing_window = QWidget()
            self.editing_window.setObjectName("editing_window")
            self.editing_window.changed_pitch = 0
            self.editing_window.warning_message_text = ""
            self.editing_window.generated_filename = ""
            self.editing_window.generated_filepath = ""
            self.editing_window.setStyleSheet("""
                        #editing_window{
                            border:none;
                            background-color:rgb(224, 254, 255);
                            background-image: url(./designer/2.png);
                        } 
                        QPushButton{
                            background-color: rgba(215, 255, 210,20);
                            border:none;
                            border-radius:11px;
                            font:  15px;
                            color: white;
                        }
                        QLabel{
                            border:none;
                        }    
                        QTextEdit{
                            border:none;
                        }





                        """)

            # Selected file name
            selected_file_name = QLabel(self.editing_window)
            selected_file_name.setGeometry(150, 30, 500, 30)
            selected_file_name.setObjectName("selected_file_name")
            displayed_file_name = self.sound_selected_filename
            print("displayed file name: ", displayed_file_name)
            if len(displayed_file_name) >= 30:
                displayed_file_name = displayed_file_name[0, 19] + "..." + displayed_file_name[-7,]
            selected_file_name.setText("Selected file name: " + displayed_file_name)

            # editing parameter
            # input_layout=QVBoxLayout()
            editing_param = QTextEdit(self.editing_window)
            font = QFont("Arial", 12)
            editing_param.setFont(font)
            editing_param.setPlaceholderText("Pitch to shift...")

            editing_param.setGeometry(50, 90, 200, 40)
            editing_param.setObjectName("editing_param")
            # input_layout.addWidge(editing_param)

            # Increment and decreament pitch
            increment_button = QPushButton(self.editing_window)
            increment_button.setGeometry(275, 90, 25, 18)
            increment_button.setText("+")
            increment_button.clicked.connect(self.increment_pitch)
            decrement_button = QPushButton(self.editing_window)
            decrement_button.setGeometry(275, 112, 25, 18)
            decrement_button.setText("-")
            decrement_button.clicked.connect(self.decrement_pitch)

            # a button to confirm input
            confirm_button = QPushButton(self.editing_window)
            confirm_button.setGeometry(450, 95, 100, 30)
            confirm_button.setText("Confirm")
            confirm_button.clicked.connect(self.handleConfirm)

            # Warning message
            warning_message = QLabel(self.editing_window)
            warning_message.setGeometry(50, 145, 500, 20)
            warning_message.setObjectName("warning_message")
            # warning_message.setText(self.editing_window.warning_message_text)

            # Generated file name
            generated_file_name = QLabel(self.editing_window)
            generated_file_name.setGeometry(50, 180, 500, 30)
            generated_file_name.setObjectName("generated_file_name")

            # Save the generated file button
            save_button = QPushButton(self.editing_window)
            save_button.setGeometry(450, 240, 100, 30)
            save_button.setText("Save")
            save_button.setObjectName("save_button")
            save_button.clicked.connect(self.handleSave)

            # show the window
            self.editing_window.setGeometry(100, 100, 600, 300)
            self.editing_window.setWindowTitle("Audio Pitch Changing")
            self.editing_window.show()

        else:
            self.editing_window.show()

    def increment_pitch(self):
        editing_param = self.editing_window.findChild(QTextEdit, "editing_param")
        editing_param_text = editing_param.toPlainText()
        editing_param_int = 0
        try:
            editing_param_int = int(editing_param_text)
            editing_param_int += 1
            editing_param_text = str(editing_param_int)
        except ValueError:
            editing_param_text = "0"

        editing_param.setText(editing_param_text)

    def decrement_pitch(self):
        editing_param = self.editing_window.findChild(QTextEdit, "editing_param")
        editing_param_text = editing_param.toPlainText()
        editing_param_int = 0
        try:
            editing_param_int = int(editing_param_text)
            editing_param_int -= 1
            editing_param_text = str(editing_param_int)
        except ValueError:
            editing_param_text = "0"

        editing_param.setText(editing_param_text)

    def handleSave(self):
        generated_file_name = self.editing_window.findChild(QLabel, "generated_file_name")
        editing_param = self.editing_window.findChild(QTextEdit, "editing_param")
        editing_param_text = int(editing_param.toPlainText())
        save_path, _ = QFileDialog.getSaveFileName(self, "Save as..?", "", "WAV FILE (*.wav)")
        if save_path:
            tone_editing(self.sound_selected_filepath, editing_param_text, save_path)

    # handle confirm: whether the shifting_pitch text button is receiving correct input
    def handleConfirm(self):
        editing_param = self.editing_window.findChild(QTextEdit, "editing_param")
        editing_param_text = editing_param.toPlainText()
        warning_message = self.editing_window.findChild(QLabel, "warning_message")
        try:
            self.text = int(editing_param_text)
            warning_message.setText("Successfully set shifting pitch.")
        except ValueError:
            warning_message.setText("Invalid shifting pitch, please enter a valid integer.")


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
            self.speech_to_text_window.setObjectName("speech_to_text_window")
            self.speech_to_text_window.transcript = ""
            self.speech_to_text_window.setStyleSheet("""
            #speech_to_text_window{
                border:none;
                background-color:rgb(224, 254, 255);
                background-image: url(./designer/2.png);
            } 
            QPushButton{
                background-color: rgba(215, 255, 210,20);
                border:none;
                border-radius:11px;
                font:  15px;
                color: white;
            }
            QLineEdit{
                border:none;
            }    
            QTextEdit{
                border:none;
            }





            """)
            # selected file name
            selected_file_name = QLineEdit(self.speech_to_text_window)
            selected_file_name.setGeometry(50, 30, 250, 30)
            selected_file_name.setReadOnly(True)
            selected_file_name.setObjectName("selected_file_name")
            selected_file_name.setText(self.sound_selected_filename)
            font = QFont("Arial", 10)
            selected_file_name.setFont(font)

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
