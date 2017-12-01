import os
import sys
import six
import subprocess
from PySide import QtCore, QtGui

from memo_ui import Ui_MainWindow

def execute_shell_in_separate_window(command):
    if os.name == 'nt':
        subprocess.Popen('start cmd /K %s' % command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen('x-terminal-emulator -hold -e "%s"' % command, shell=True)


class Memo(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Memo, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # tray & menu
        self.createNewAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-new"),
                                  '&Create new collection', self)
        self.createNewAction.triggered.connect(self.createDatabase)

        self.loadAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-open"),
                                '&Load collection from file', self)
        self.loadAction.setShortcut('Ctrl+O')
        self.loadAction.setStatusTip('Opening File')
        self.loadAction.triggered.connect(self.loadDatabase)

        self.saveAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-save"),
                                 '&Save collection into file', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Saving File')
        self.saveAction.triggered.connect(self.saveDatabase)

        self.saveAsAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-save-as"),
                                  '&Save collection into new file', self)
        self.saveAsAction.setStatusTip('Saving File')
        self.saveAsAction.triggered.connect(self.saveAsDatabase)

        self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme("help-about"),
                                    '&About', self)
        self.aboutAction.triggered.connect(self.about)

        self.quitAction = QtGui.QAction(QtGui.QIcon.fromTheme("application-exit"),
                                        '&Quit', self)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('Exit application')
        self.quitAction.triggered.connect(self.close)

        self.fileMenu = self.ui.menubar.addMenu('&File')
        self.fileMenu.addAction(self.createNewAction)
        self.fileMenu.addAction(self.loadAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.aboutAction)
        self.fileMenu.addAction(self.quitAction)

        # table header
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["", "", "alias", "command"])
        self.ui.tableWidget.setVisible(False)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.ui.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.tableWidget.setVisible(True)

        self.ui.lineEditPath.setReadOnly(True)

        # connect
        self.ui.tableWidget.cellChanged.connect(self.update)
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.lineEditSearch.textEdited.connect(self.filter)

        self.onStart()

    def onStart(self):
        self.file = ""
        self.aliases = [] # [[name, alias]]
        self.homeDir = os.path.join(os.path.expanduser("~"), "Memo")
        if not os.path.exists(self.homeDir):
            os.makedirs(self.homeDir)
        if not os.path.exists(os.path.join(self.homeDir, "aliases.txt")):
            self.createDatabase(os.path.join(self.homeDir, "aliases.txt"))
        else:
            self.loadDatabase(os.path.join(self.homeDir, "aliases.txt"))

    def createDatabase(self, file=''):
        if self.file and self.savePageBeforeClose() == -1:
            return 0
        try:
            if not file:
                file = str(self.showFileSaveDialog()[0])
            if file:
                with open(file, 'a') as f:
                    f.write("unix-hello-world    echo 'hello world! :)'" + os.linesep)
                self.loadDatabase(file)
        except: self.showCritical("Error","Can't create %s" % file)

    def loadDatabase(self, file=""):
        if self.file and self.savePageBeforeClose() == -1:
            return 0
        back_file = self.file
        back_aliases = self.aliases
        if not file:
            file = self.showFileOpenDialog()[0]
        if file:
            try:
                with open(file, 'r') as f:
                    self.aliases = [ l.rstrip('\n\r').split('    ') for l in f.readlines() if (l[0] != '#' and '    ' in l)]
                self.fillTable(self.aliases)
                self.ui.lineEditPath.setText(file)
                self.file = file
            except:
                self.showCritical("Some error with set db", "Some error occurred when opening %s as database" 
                        %(self.file))
                self.file = ''
                self.aliases = back_aliases
                self.fillTable(self.aliases)

    def fillTable(self, aliases):
        self.ui.tableWidget.setVisible(False)
        # clear table
        self.ui.tableWidget.clearContents()
        # set content
        self.ui.tableWidget.setRowCount(len(aliases))
        for row, item in enumerate(aliases):
            button = QtGui.QPushButton(QtGui.QIcon.fromTheme("edit-delete"), "")
            button.setFixedSize(50, 50)
            button.clicked.connect(self.delete)
            button.setProperty("row",row)
            self.ui.tableWidget.setCellWidget(row, 0, button)
            button = QtGui.QPushButton(QtGui.QIcon.fromTheme("media-playback-start"), "")
            button.setFixedSize(50, 50)
            button.clicked.connect(self.shell)
            button.setProperty("row",row)
            self.ui.tableWidget.setCellWidget(row, 1, button)
            self.ui.tableWidget.setItem(row, 2, QtGui.QTableWidgetItem(item[0]))
            self.ui.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem(item[1]))
            self.ui.tableWidget.setRowHidden(row, False)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.setVisible(True)

    def update(self, row, column):
        text = self.ui.tableWidget.item(row, column).text()
        self.aliases[row][column-2] = text

    def delete(self):
        row = self.sender().property("row")
        del self.aliases[row]
        self.fillTable(self.aliases)

    def add(self):
        self.aliases.append(["", ""])
        self.fillTable(self.aliases)
        self.ui.tableWidget.scrollToBottom()

    def shell(self):
        row = self.sender().property("row")
        item = self.ui.tableWidget.item(row, 3)
        text = item.text()
        execute_shell_in_separate_window(text)

    def filter(self):
        text = self.ui.lineEditSearch.text()
        if text:
            for row in xrange(len(self.aliases)):
                if (text not in self.ui.tableWidget.item(row, 2).text() or
                   text not in self.ui.tableWidget.item(row, 3).text()):
                    self.ui.tableWidget.setRowHidden(row, True)
                else:
                    self.ui.tableWidget.setRowHidden(row, False)
        else:
            for row in xrange(len(self.aliases)):
                self.ui.tableWidget.setRowHidden(row, False)

    def saveDatabase(self):
        self.saveAsDatabase(self.file)

    def saveAsDatabase(self, file):
        if len(self.aliases):
            if not file:
                file = self.showFileSaveDialog()[0]
            if file:
                try:
                    with open(file, 'w') as f:
                        # miss commented out lines
                        f.writelines([ "    ".join(i) +  os.linesep for i in self.aliases])
                    self.file = file
                    if file[-4:] == '.txt':
                        file = file[0:-4]
                    with open(file + '.sh', 'w') as f:
                        f.writelines([ "alias %s='%s'%s" % (i[0], i[1].replace("'", r"\'"), os.linesep) for i in self.aliases])
                    with open(file + '.cmd', 'w') as f:
                        f.writelines([ "doskey %s=%s%s" % (i[0], i[1], os.linesep) for i in self.aliases])
                except: raise;self.showCritical("Error","Can't save %s" % file)

    def about(self):
        about = """
A simple program for manage shell aliases and commands.
Created by Filipp Kucheryavy for his friend Vladimir Kataev :)
License: MIT
src: github.com/Friz-zy/Memo
                """
        self.showMessage("About Memo", about)

    def savePageBeforeClose(self):
        if len(self.aliases):
            q = "Do you want to save your changes?"
            if self.file:
                q = "Do you want to save your changes as %s?" % self.file
            choice = self.showChoice("?!", q)
            if choice == -1:
                return -1
            elif choice:
                self.saveDatabase()
            return 1

    def showChoice(self, title, text):
        q = QtGui.QMessageBox.question(self, 
                  title,
                  text,
                  QtGui.QMessageBox.No |
                  QtGui.QMessageBox.Cancel |
                  QtGui.QMessageBox.Yes,)
        if q == QtGui.QMessageBox.Yes:
            return True
        elif q == QtGui.QMessageBox.No:
            return False
        return -1

    def showFileOpenDialog(self, path="", filer=""):
        if not path:
            path = self.homeDir
        return QtGui.QFileDialog.getOpenFileName(self,
                      'Open file', path, filer)

    def showFileSaveDialog(self, path="", filer=""):
        if not path:
            path = self.homeDir
        return QtGui.QFileDialog.getSaveFileName(self,
                    'Save file as:', path, filer)

    def showMessage(self, title, text):
        QtGui.QMessageBox.information(self, str(title), str(text))

    def showCritical(self, title, text):
        QtGui.QMessageBox.critical(self, str(title), str(text))

    def closeEvent(self, e):
        if self.savePageBeforeClose() != -1:
            six.print_(("bye!"), file=sys.stdout, end="\n", sep=" ")
            self.close()
        else:
            e.ignore()


def main():
    app = QtGui.QApplication(sys.argv)
    myapp = Memo()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
