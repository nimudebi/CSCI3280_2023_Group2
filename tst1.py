from SoundRecorder import SoundRecorder
import sys
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QTimer, QUrl, Qt
app = QApplication(sys.argv)

chat_app = SoundRecorder()
chat_app.show()
sys.exit(app.exec_())