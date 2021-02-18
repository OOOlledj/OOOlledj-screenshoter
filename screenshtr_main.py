import pyautogui as pyAG
import keyboard
import time, os, sys, traceback
from PyQt5.QtWidgets import \
    QApplication, QLabel, QWidget, \
    QPushButton, QVBoxLayout, QLineEdit, \
    QFileDialog, QHBoxLayout, QMainWindow

class QtScreenshoter(QMainWindow):

    def __init__(self):

        super(QtScreenshoter, self).__init__()

        #block 1:
        self.mainWindow = QWidget()
        self.mainWindow.resize(250,150)

        commonLayout = QVBoxLayout()
        layoutPath = QHBoxLayout()
        layoutHotk = QHBoxLayout()
        layoutSnap = QHBoxLayout()
        layoutStat = QHBoxLayout()

        #block 2:
        self.pathString = QLineEdit(os.getenv("HOME"))
        layoutPath.addWidget(self.pathString)
        self.pathString.setFixedWidth(200)
        self.pathString.setFixedHeight(20)
        ### interruption start
        self.snapButton = QPushButton('Screen!!!')
        layoutSnap.addWidget(self.snapButton)
        self.snapButton.clicked.connect(self.makeTheSnap)
        ### interruption end

        #block 3:
        self.foldButton = QPushButton('Submit folder')
        layoutPath.addWidget(self.foldButton)
        self.foldButton.setFixedWidth(130)
        self.foldButton.setFixedHeight(20)
        self.foldButton.clicked.connect(self.submitFolder)# connect the submission of the folder

        #block 4:
        self.hotkString = QLineEdit('alt+shift+p')
        layoutHotk.addWidget(self.hotkString)
        self.hotkString.setFixedWidth(200)
        self.hotkString.setFixedHeight(20)

        self.hotkButton = QPushButton('Submit hotkey')
        layoutHotk.addWidget(self.hotkButton)
        self.hotkButton.setFixedWidth(130)
        self.hotkButton.setFixedHeight(20)
        self.hotkButton.clicked.connect(self.submitHotkey)# connect the submission of the hotkey

        #block 5:
        self.statusStringLabel = QLabel('STATUS:')
        self.statusFolderLabel = QLabel('Folder OK')
        self.statusHotkeyLabel = QLabel('Hotkey OK')
        layoutStat.addWidget(self.statusStringLabel)
        layoutStat.addWidget(self.statusFolderLabel)
        layoutStat.addWidget(self.statusHotkeyLabel)

        #final block:
        commonLayout.addLayout(layoutPath)
        commonLayout.addLayout(layoutHotk)
        commonLayout.addLayout(layoutSnap)
        commonLayout.addLayout(layoutStat)
        self.mainWindow.setLayout(commonLayout)

    def submitFolder(self):
        #code = None
        if os.path.exists(self.pathString.text()):
            self.snapButton.clicked.connect(self.makeTheSnap) #unlocking the snap button
            code = 'Folder OK'
        else:
            code = 'Folder error'
            self.snapButton.clicked.connect(self.submitFolder)  # blocking the snap button
        self.statusFolderLabel.setText(code)

    def submitHotkey(self):
        #code = None
        self.keyActual = self.hotkString.text()
        try:
            keyboard.remove_hotkey(self.KeyActual)
        except:
            pass

        try:
            keyboard.add_hotkey(self.keyActual, self.makeTheSnap)
            code = 'Hotkey OK'
        except Exception:
            traceback.print_exc()
            code = 'Hotkey error'
        finally:
            self.statusHotkeyLabel.setText(code)

    def makeTheSnap(self):
        cTime = time.time()
        milSec = round(cTime * 1000) % 1000
        ScreenName = time.strftime('%d%m%Y-%H%M%S-') + str(milSec) + '.png'

        toThePath = self.pathString.text() +  '//'  + ScreenName
        pyAG.screenshot().save(toThePath)

if __name__ == '__main__':
    app = QApplication([])
    application = QtScreenshoter()
    application.mainWindow.show()
    sys.exit(app.exec())