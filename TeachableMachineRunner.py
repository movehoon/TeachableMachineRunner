import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageOps
import tm_model

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.tm = tm_model.TM_Model('keras_model.h5')
        # image = Image.open('cat.jpg')
        # self.tm.predict(image)

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

        grid.addWidget(QLabel('Load Model:'), 0, 0)
        grid.addWidget(QLabel('Open Image:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)
        grid.addWidget(QLabel('Result:'), 3, 0)

        grid.addWidget(btnModelOpen, 0, 1)
        grid.addWidget(btnImageOpen, 1, 1)
        grid.addWidget(self.imageLabel, 2, 1)
        grid.addWidget(self.textResult, 3, 1)

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
            self.textResult.setText(str(self.tm.predict(image)))
            # print('result: ', result)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())