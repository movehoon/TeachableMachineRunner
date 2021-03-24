import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PIL import Image, ImageOps
import tm_model
from flask import Flask, request, Response
from pathlib import Path

flask_app = Flask(__name__)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.threshold = 0.9
        self.initUI()
        # self.tm = tm_model.TM_Model('keras_model.h5')

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Line1. Keras Model Open
        btnModelOpen = QPushButton('Model Open', self)
        btnModelOpen.clicked.connect(self.modelOpen)
        self.labelModelName = QLabel('model_name')
        # Line2. Image Open
        btnImageOpen = QPushButton('Image Open', self)
        btnImageOpen.clicked.connect(self.imageOpen)
        self.labelImageName = QLabel('image_name')
        # Line3. Image Show
        self.imageLabel = QLabel()
        # Line4. Threshold
        self.labelThreshold = QLabel('Threshold('+str(int(self.threshold*100))+')')
        self.sliderThreshold = QSlider(Qt.Horizontal, self)
        self.sliderThreshold.setRange(0, 100)
        self.sliderThreshold.setSingleStep(1)
        self.sliderThreshold.setValue(self.threshold*100)
        self.sliderThreshold.setTickPosition(QSlider.NoTicks)
        self.sliderThreshold.valueChanged.connect(self.changeThreshold)
        # Line5. Show Result
        self.textResult = QTextEdit()
        # Line6. Server Start
        self.btnStartServer = QPushButton('Server Start', self)
        self.btnStartServer.clicked.connect(self.startServer)
        self.labelServerState = QLabel('Server Stop')

        # Column 1
        grid.addWidget(QLabel('Load Model:'), 0, 0)
        grid.addWidget(QLabel('Open Image:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)
        grid.addWidget(self.labelThreshold, 3, 0)
        grid.addWidget(QLabel('Result:'), 4, 0)
        grid.addWidget(QLabel('Server Run:'), 5, 0)

        # Column 2
        grid.addWidget(btnModelOpen, 0, 1)
        grid.addWidget(btnImageOpen, 1, 1)
        grid.addWidget(self.imageLabel, 2, 1)
        grid.addWidget(self.sliderThreshold, 3, 1)
        grid.addWidget(self.textResult, 4, 1)
        grid.addWidget(self.btnStartServer, 5, 1)

        # Column 3
        grid.addWidget(self.labelModelName, 0, 2)
        grid.addWidget(self.labelImageName, 1, 2)
        grid.addWidget(self.labelServerState, 5, 2)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def modelOpen(self):
        model_path = QFileDialog.getOpenFileName(self, 'Open Model', './')
        print(model_path)
        if len(model_path[0]):
            self.labelModelName.setText(Path(model_path[0]).name)
            self.tm = tm_model.TM_Model(model_path[0])

    def imageOpen(self):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './')
        print(image_path)
        if len(image_path[0]):
            self.labelImageName.setText(Path(image_path[0]).name)
            self.imageLabel.setPixmap(QPixmap(image_path[0]))
            image = Image.open(image_path[0]).convert('RGB')
            result = self.predict(image)
            self.textResult.setText(str(result))
            # print('result: ', result)
        return 0

    def changeThreshold(self):
        self.labelServerState.setText('Server Running')
        self.threshold = float(self.sliderThreshold.value())/100
        self.labelThreshold.setText('Threshold('+str(int(self.threshold*100))+')')
        # print(self.threshold)
        return 0

    def predict(self, image):
        return self.tm.predict(image, self.threshold)

    def startServer(self):
        print('startServer')
        self.thread = QThread()
        self.tmServer = TM_Server()
        self.tmServer.moveToThread(self.thread)
        self.thread.started.connect(self.tmServer.run)
        self.thread.start()
        self.btnStartServer.setEnabled(False)
        # global flask_app
        # flask_app.run()
        return 0

class TM_Server(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        print('run Flask')

        global flask_app
        flask_app.run()

        self.finished.emit()

@flask_app.route("/")
def index():
    return "This is TeachableMachine Server."

@flask_app.route('/tms', methods=['POST'])
def teachablemachine():
    if request.method == 'POST':
        f = request.files['image']

        image = Image.open(f).convert('RGB')
        result = ex.predict(image)
        print('result: ', result)
        return str(result)
    return 'NOT_FOUND'

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

