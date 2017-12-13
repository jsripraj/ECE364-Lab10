import sys

from PySide.QtGui import *
from PySide.QtCore import *
from BasicUI import *
from pprint import pprint as pp
import re

class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Consumer, self).__init__(parent)
        self.setupUi(self)

        self.btnSave.setEnabled(False)
        self.btnClear.clicked.connect(self.clearForm)
        for name in self.__dict__:
            if re.match(r"txt", name):
                getattr(self, name).textChanged.connect(self.toggleBtns)
        self.cboCollege.currentIndexChanged.connect(self.toggleBtns)
        self.chkGraduate.stateChanged.connect(self.toggleBtns)
        self.btnSave.clicked.connect(self.saveFile)
        self.btnLoad.clicked.connect(self.loadData)

    def saveFile(self):
        content = '<?xml version="1.0" encoding="UTF-8"?>\n<Content>\n'
        isGrad = 'false'
        if self.chkGraduate.checkState():
            isGrad = 'true'
        content += '\t<StudentName graduate="{}">{}</StudentName>\n'.format(isGrad, self.txtStudentName.text())
        content += '\t<StudentID>{}</StudentID>\n'.format(self.txtStudentID.text())
        content += '\t<College>{}</College>\n'.format(self.cboCollege.currentText())
        content += '\t<Components>\n'
        for i in range(1, 21):
            nameVar = 'txtComponentName_{}'.format(i)
            countVar = 'txtComponentCount_{}'.format(i)
            if getattr(self, nameVar).text() or getattr(self, countVar).text():
                content += '\t\t<Component name="{}" count="{}" />\n'.format(getattr(self, nameVar).text(), getattr(self, countVar).text())
        content += '\t</Components>\n</Content>'
        with open('target.xml', 'w') as mf:
            mf.write(content)
        self.btnSave.setEnabled(False)

    def toggleBtns(self):
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)

    def clearForm(self):
        for name in self.__dict__:
            if re.match(r"txt", name):
                getattr(self, name).setText(None)
        self.cboCollege.setCurrentIndex(0)
        self.chkGraduate.setCheckState(Qt.Unchecked)
        self.btnSave.setEnabled(False)
        self.btnLoad.setEnabled(True)

    def getCollegeIndexDict(self):
        collegeIndexDict = {}
        collegeIndexDict['-----'] = 0
        collegeIndexDict['Aerospace Engineering'] = 1
        collegeIndexDict['Civil Engineering'] = 2
        collegeIndexDict['Computer Engineering'] = 3
        collegeIndexDict['Electrical Engineering'] = 4
        collegeIndexDict['Industrial Engineering'] = 5
        collegeIndexDict['Mechanical Engineering'] = 6
        return collegeIndexDict

    def loadDataFromFile(self, filePath):
        """
        Handles the loading of the data from the given file name. This method will be invoked by the 'loadData' method.
        
        *** YOU MUST USE THIS METHOD TO LOAD DATA FILES. ***
        *** This method is required for unit tests! ***
        """
        with open(filePath, 'r') as mf:
            content = mf.read()
        expr = r'<StudentName graduate="(?P<isGrad>[^"]*)">(?P<name>[^<>]*)</StudentName>\s*' \
               r'<StudentID>(?P<id>[^<>]*)</StudentID>\s*' \
               r'<College>(?P<college>[^<>]*)</College>\s*'
        m = re.search(expr, content, re.IGNORECASE)
        if m.group('isGrad') == 'true':
            self.chkGraduate.setCheckState(Qt.Checked)
        self.txtStudentName.setText(m.group('name'))
        self.txtStudentID.setText(m.group('id'))
        collegeIndexdict = self.getCollegeIndexDict()
        self.cboCollege.setCurrentIndex(collegeIndexdict[m.group('college')])
        expr = r'<Component name="(?P<compName>[^"]*?)" count="(?P<compCount>[^"]*?)" />'
        m = re.findall(expr, content)
        i = 1
        for name, count in m:
            getattr(self, 'txtComponentName_'+str(i)).setText(name)
            getattr(self, 'txtComponentCount_'+str(i)).setText(count)
            i += 1
            if i > 20:
                break
        self.btnLoad.setEnabled(False)
        self.btnSave.setEnabled(True)

    def loadData(self):
        """
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        *** DO NOT MODIFY THIS METHOD! ***
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.xml)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()
