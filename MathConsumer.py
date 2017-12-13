# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *

from calculator import *
import re

class MathConsumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MathConsumer, self).__init__(parent)
        self.setupUi(self)
        self.btnCalculate.clicked.connect(self.performOperation)

    def performOperation(self):
        num1 = self.edtNumber1.text()
        num2 = self.edtNumber2.text()
        try:
            if re.match(r"^-?[0-9]*\.[0-9]+\s*$", num1) or re.match(r"^-?[0-9]*\.[0-9]+\s*$", num2):
                num1 = float(num1)
                num2 = float(num2)
            else:
                num1 = int(num1)
                num2 = int(num2)
        except:
            self.edtResult.setText('E')
            return
        op = self.cboOperation.currentText()
        if op == '+':
            self.edtResult.setText("{}".format(num1 + num2))
        elif op == '-':
            self.edtResult.setText("{}".format(num1 - num2))
        elif op == '*':
            self.edtResult.setText("{}".format(num1 * num2))
        else:
            try:
                self.edtResult.setText("{}".format(num1 / num2))
            except:
                self.edtResult.setText('E')

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MathConsumer()

    currentForm.show()
    currentApp.exec_()
