# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
import sys
import os
import psycopg2 as pg
import matplotlib.pyplot as plt
import json
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap, QImage
import shutil
from PIL import Image


import MainWin
from yolov5.detect import run

def plot_dots(path, dots):
    fig = plt.figure(frameon=False)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.axis('off')
    fig.add_axes(ax)

    im = plt.imread(path)
    ax.imshow(im, aspect='auto')
    ax.plot(dots[0], dots[1],'.r', ms = 4)
    fig.savefig('res.png')

    
def get_dots(txt_path, img_path):
    im = Image.open(img_path)
    (width, height) = im.size

    with open(txt_path) as f:
        lines = f.readlines()

        dots_x = []
        dots_y = []

        for obj in lines:
            coord = obj.split(" ")
            x = float(coord[1])*width
            y = float(coord[2])*height
            dots_x.append(float(x))
            dots_y.append(float(y))
            
        return [dots_x, dots_y]

class Main(QMainWindow, MainWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.funk(self.lineEdit.text()))

    def funk(self, file_name):
        #!python detect.py --source ../Road_Sign_Dataset/images/test/ --weights runs/train/yolo_road_det/weights/best.pt --conf 0.25 --name yolo_road_det
        dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        shutil.rmtree(dir + '\\res', ignore_errors=True)
        pred = run(source = dir + "\\" + file_name + '.jpg', 
            weights= dir + '\\best.pt', 
            conf_thres = 0.15, 
            name = 'res', 
            iou_thres = 0.2,
            save_txt = True,
            project = dir)

        txt_path = dir + '\\res\labels\\' + file_name + ".txt"
        img_path = dir + "\\" + file_name + '.jpg'

        dots = get_dots(txt_path, img_path)
        plot_dots(img_path, dots)

        self.label.setPixmap(QPixmap(dir + "\\res.png"))
        self.label_3.setText("Num of walruses: \n" + str(len(dots[0])))


def main():
    x = QApplication(sys.argv)
    window = Main()
    window.show()
    x.exec_()

main()
