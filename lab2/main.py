import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import pymysql
import hashlib
from lab2 import Ui_MainWindow


class Login(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login)  # 绑定登录按钮
        self.pushButton_2.clicked.connect(self.close)  # 绑定退出按钮

    def login(self):
        userid = self.lineEdit.text()
        password = self.lineEdit_2.text()

        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123456",
            db="testdb",
            port=3306
        )
        cur = conn.cursor()
        cur.execute("SELECT user_passwd, IsAdmin FROM tbuser WHERE user_id=%s", (userid,))
        row = cur.fetchone()

        if row is None:
            QMessageBox.warning(self, "警告", "无此用户！")
        else:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            if row[0] == md5.hexdigest():
                if row[1] == 1:
                    QMessageBox.information(self, "提示", "管理员登录成功！")
                else:
                    QMessageBox.information(self, "提示", "用户登录成功！")
            else:
                QMessageBox.warning(self, "警告", "用户名或密码错误！")

        cur.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
