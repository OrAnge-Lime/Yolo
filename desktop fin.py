# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QFileDialog
import sys
import os
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap, QImage
import shutil
from PIL import Image
import MainWin
import cv2
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
        self.pushButton.clicked.connect(lambda: self.funk())

    def funk(self):
        #!python detect.py --source ../Road_Sign_Dataset/images/test/ --weights runs/train/yolo_road_det/weights/best.pt --conf 0.25 --name yolo_road_det

        try:
            dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

            imagesPaths = list(filter(lambda x: x.split(".")[1] == "jpg", os.listdir(dirlist)))
        except:
            return

        shutil.rmtree(dir + '\\res', ignore_errors=True)

        if imagesPaths:
            images = []

            for imagePath in imagesPaths:
                image = cv2.imread(dirlist + "//" + imagePath)
                images.append(image)

            stitcher = cv2.Stitcher_create()
            (status, stitched) = stitcher.stitch(images)

            if status == 0:
                cv2.imwrite(dir + "//stitched.jpg", stitched)
                imagesPaths = ["stitched.jpg"]
                dirlist = dir

            count = 0

            pred = run(source=dirlist,
                       weights=dir + '\\best.pt',
                       conf_thres=0.15,
                       name='res',
                       iou_thres=0.2,
                       save_txt=True,
                       project=dir)

            for image in imagesPaths:
                txt_path = dir + '//res//labels//' + image.split(".")[0] + ".txt"

                dots = get_dots(txt_path, dirlist + "//" + image)
                plot_dots(dirlist + "//" + image, dots)
                self.label.setPixmap(QPixmap(dir + "\\res.png"))
                count += len(dots[0])

            self.label_3.setText("Num of walruses: \n" + str(count))

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('В папке нет фотографий с разрешением .jpg')
            msg.setWindowTitle("Error")
            msg.exec_()


def main():
    x = QApplication(sys.argv)
    window = Main()
    window.show()
    x.exec_()

main()
