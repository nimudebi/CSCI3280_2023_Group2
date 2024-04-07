from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.Qt import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer, QUrl, Qt
import qtawesome as qta
from karaokeUI import *
import pyaudio
from write_wav_file import write_wav_file
import sys
import os
import karaoke_function as k
class Karaoke(QMainWindow):

    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.timing = QTimer()
        self.filepath = None
        self.filename = None
        self.sound_player = QMediaPlayer()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.showMinimized)
        self.ui.pushButton.clicked.connect(self.close)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # initialize the variablesspeed
        self.sound_selected_filepath = None
        self.sound_selected_filename = None
        self.sound_selected = QMediaPlayer()

        # closing and full-screen displaying button
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.showMinimized)
        self.ui.pushButton.clicked.connect(self.close)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # player slider
        self.sound_player.setVolume(66)
        self.ui.horizontalSlider.setDisabled(True)
        self.ui.pushButton_5.setEnabled(False)
        self.sound_player.positionChanged.connect(self.update_play_slider)
        self.sound_player.mediaStatusChanged.connect(self.final)
        self.ui.horizontalSlider.sliderMoved.connect(self.playing_adjusting)
        self.ui.horizontalSlider.sliderReleased.connect(self.playing_adjusted)

        # audio playing button
        self.ui.pushButton_6.clicked.connect(self.switch_to_previous_audio)
        self.ui.pushButton_4.clicked.connect(self.switch_to_next_audio)
        self.ui.pushButton_6.setDisabled(True)
        self.ui.pushButton_4.setDisabled(True)
        self.flag_any_audio_file_selected = False

        # Recording button
        self.recording = False
        self.ui.pushButton_9.clicked.connect(self.record_change)

        # input file button & music list
        self.ui.pushButton_11.clicked.connect(self.load_audio)
        self.ui.listWidget.itemClicked.connect(self.audio_selected)
        self.ui.listWidget.itemDoubleClicked.connect(self.audio_play)
        self.ui.listWidget.setContextMenuPolicy(3)
        self.ui.listWidget.customContextMenuRequested.connect(self.show_menu)


    # function for sound player slider
    def update_play_slider(self, position):
        duration = self.sound_player.duration()
        self.ui.horizontalSlider.setRange(0, duration)
        self.ui.horizontalSlider.setValue(position)
        self.ui.horizontalSlider.setDisabled(False)
    def playing_adjusting(self, position):
        self.sound_player.pause()
        self.sound_player.setPosition(position)
    def playing_adjusted(self):
        if self.playing:
            self.sound_player.play()

    # Function for input file and music list
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

    def load_audio(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio Files (*.mp3 *.wav *.ogg *.flac *.aac)")
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            for filename in filenames:
                accompaniment_name = os.path.splitext(os.path.basename(filename))[0]
                proceeded_filename = k.karaoke_bgm(os.path.abspath(filename))
                print(proceeded_filename)
                item = QListWidgetItem(accompaniment_name)
                item.setData(Qt.UserRole, proceeded_filename)
                self.ui.listWidget.addItem(item)

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

    def audio_selected(self, item):
        self.change_label = False
        self.sound_selected_filename = item.text()
        self.sound_selected_filepath = item.data(Qt.UserRole)
        m = QMediaContent(QUrl.fromLocalFile(self.sound_selected_filepath))
        self.sound_selected.setMedia(m)

        if not self.flag_any_audio_file_selected:
            self.ui.pushButton_6.setDisabled(False)
            self.ui.pushButton_4.setDisabled(False)
            self.flag_any_audio_file_selected = True

    def audio_play(self, item):
        self.filename = item.text()
        self.filepath = item.data(Qt.UserRole)
        media_content = QMediaContent(QUrl.fromLocalFile(self.filepath))
        self.sound_player.setMedia(media_content)
        self.ui.pushButton_5.setEnabled(True)
        self.playing = True
        self.sound_player.play()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./designer/circle-pause-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_5.setIcon(icon)

    # function for recording button
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

    def final(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_change()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat_app = Karaoke()
    chat_app.show()
    sys.exit(app.exec_())