# Qt Backup Tool
#
# by: @acgissues
#
# This tool helps making .tar.gz archives from specified directories.

import sys, tarfile, os
from gui import AMainWindow
from PySide2.QtWidgets import (QFileDialog, QMainWindow, QDesktopWidget,
    QApplication)

class OpenFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)

        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.ShowDirsOnly, True)

class MainWindow(QMainWindow, AMainWindow.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.center()

        self.btnDocuments.clicked.connect(self.openFile)
        self.btnMusic.clicked.connect(self.openFile)
        self.btnVideos.clicked.connect(self.openFile)
        self.btnImages.clicked.connect(self.openFile)
        self.btnBackup.clicked.connect(self.backup)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile(self):
        openFileDialog = OpenFileDialog()
        openFileDialog.show()

        sender = self.sender()

        if openFileDialog.exec_():
            if sender.objectName() == 'btnDocuments':
                self.txtDocuments.setText(openFileDialog.selectedFiles().pop())
            elif sender.objectName() == 'btnMusic':
                self.txtMusic.setText(openFileDialog.selectedFiles().pop())
            elif sender.objectName() == 'btnVideos':
                self.txtVideos.setText(openFileDialog.selectedFiles().pop())
            elif sender.objectName() == 'btnImages':
                self.txtImages.setText(openFileDialog.selectedFiles().pop())

    def backup(self):
        checkedDocuments = self.chkDocuments.isChecked()
        checkedMusic = self.chkMusic.isChecked()
        checkedVideos = self.chkVideos.isChecked()
        checkedImages = self.chkImages.isChecked()

        if not(checkedDocuments or checkedMusic or checkedVideos or
            checkedImages):
            self.statusBar().showMessage('Please choose a directory to backup')

        if checkedDocuments and self.txtDocuments.text() != '':
            self.make_tarfile('documents.tar.gz', self.txtDocuments.text())
        if checkedMusic:
            self.make_tarfile('music.tar.gz', self.txtMusic.text())
        if checkedVideos:
            self.make_tarfile('videos.tar.gz', self.txtVideos.text())
        if checkedImages:
            self.make_tarfile('images.tar.gz', self.txtImages.text())

    def make_tarfile(self, output_filename, source_dir):
        # self.statusBar().showMessage(output_filename + ' is backing up.')
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        self.statusBar().showMessage("{} is ready".format(output_filename))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
