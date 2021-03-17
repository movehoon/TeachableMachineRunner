import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageOps
import tm_model
from flask import Flask, request, Response

flask_app = Flask(__name__)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.tm = tm_model.TM_Model('keras_model.h5')

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Line1. Keras Model Open
        btnModelOpen = QPushButton('Model Open', self)
        btnModelOpen.clicked.connect(self.modelOpen)
        # Line2. Image Open
        btnImageOpen = QPushButton('Image Open', self)
        btnImageOpen.clicked.connect(self.imageOpen)
        # Line3. Image Show
        self.imageLabel = QLabel()
        # Line4. Show Result
        self.textResult = QTextEdit()
        # Line2. Server Start
        btnStartServer = QPushButton('Server Start', self)
        btnStartServer.clicked.connect(self.startServer)

        grid.addWidget(QLabel('Load Model:'), 0, 0)
        grid.addWidget(QLabel('Open Image:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)
        grid.addWidget(QLabel('Result:'), 3, 0)
        grid.addWidget(QLabel('Server Run:'), 4, 0)

        grid.addWidget(btnModelOpen, 0, 1)
        grid.addWidget(btnImageOpen, 1, 1)
        grid.addWidget(self.imageLabel, 2, 1)
        grid.addWidget(self.textResult, 3, 1)
        grid.addWidget(btnStartServer, 4, 1)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def modelOpen(self):
        model_path = QFileDialog.getOpenFileName(self, 'Open Model', './')
        print(model_path)
        if len(model_path[0]):
            self.tm = tm_model.TM_Model(model_path[0])

    def imageOpen(self):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './')
        print(image_path)
        if len(image_path[0]):
            self.imageLabel.setPixmap(QPixmap(image_path[0]))
            image = Image.open(image_path[0])
            result = self.predict(image)
            self.textResult.setText(str(result))
            # print('result: ', result)
        return 0

    def predict(self, image):
        return self.tm.predict(image)

    def startServer(self):
        global flask_app
        flask_app.run()
        return 0



@flask_app.route("/")
def index():
    return "hi"

@flask_app.route('/tm', methods=['POST'])
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

