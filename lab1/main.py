import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from lab1 import Ui_mainWindow


class Calculator(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setupUi(self)
        self.label_2.setText("无")

        self.operator_text = ""

        self.pushButton_13.clicked.connect(lambda: self.addDigit('1'))
        self.pushButton_14.clicked.connect(lambda: self.addDigit('2'))
        self.pushButton_15.clicked.connect(lambda: self.addDigit('3'))
        self.pushButton_16.clicked.connect(lambda: self.addDigit('4'))
        self.pushButton_10.clicked.connect(lambda: self.addDigit('6'))
        self.pushButton_12.clicked.connect(lambda: self.addDigit('8'))
        self.pushButton_9.clicked.connect(lambda: self.addDigit('5'))
        self.pushButton_11.clicked.connect(lambda: self.addDigit('7'))
        self.pushButton_4.clicked.connect(lambda: self.addDigit('0'))

        self.pushButton_3.clicked.connect(lambda: self.operator('-'))
        self.pushButton.clicked.connect(lambda: self.operator('+'))
        self.pushButton_5.clicked.connect(lambda: self.operator('*'))
        self.pushButton_6.clicked.connect(lambda: self.operator('/'))

        self.pushButton_7.clicked.connect(self.reset)
        self.pushButton_8.clicked.connect(self.calculate)

    def addDigit(self, digit):
        text = self.label.text()
        if text == '0':
            self.label.setText(digit)
        else:
            self.label.setText(text + digit)
        self.operator_text += digit
        self.label_2.setText(self.operator_text)

    def operator(self, op):
        self.op = op
        self.num1 = int(self.label.text())
        self.label.setText('0')
        self.operator_text += op
        self.label_2.setText(self.operator_text)

    def calculate(self):
        num2 = int(self.label.text())
        if self.op == '+':
            result = self.num1 + num2
        elif self.op == '-':
            result = self.num1 - num2
        elif self.op == '*':
            result = self.num1 * num2
        elif self.op == '/':
            if num2 == 0:
                # QMessageBox.warning(self, '警告', '除数不能为零')
                self.label.setText('除数不能为0')
                return
            result = self.num1 / num2
        else:
            return
        self.label.setText(str(result))

    def reset(self):
        self.label.setText('0')
        self.operator_text = ""
        self.label_2.setText("无")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
