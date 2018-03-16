# Qt Backup Tool
#
# by: @acgissues
#
# This tool helps making .tar.gz archives from specified directories.

import sys, tarfile, os
from PySide.QtGui import *
from gui import AMainWindow

class OpenFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)

        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.ShowDirsOnly, True)

        self.show()

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


        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile(self):
        openFileDialog = OpenFileDialog()

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
        if not(self.chkDocuments.isChecked() or
                self.chkMusic.isChecked() or
                self.chkVideos.isChecked() or
                self.chkImages.isChecked()):
            self.statusBar().showMessage('Please choose a directory to backup')
            return

        if self.chkDocuments.isChecked() and self.txtDocuments.text() != '':
            self.make_tarfile('documents.tar.gz', self.txtDocuments.text())
        if self.chkMusic.isChecked():
            self.make_tarfile('music.tar.gz', self.txtMusic.text())
        if self.chkVideos.isChecked():
            self.make_tarfile('videos.tar.gz', self.txtVideos.text())
        if self.chkImages.isChecked():
            self.make_tarfile('images.tar.gz', self.txtImages.text())

    def make_tarfile(self, output_filename, source_dir):
        # self.statusBar().showMessage(output_filename + ' is backing up.')
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        self.statusBar().showMessage(output_filename + ' is ready.')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
