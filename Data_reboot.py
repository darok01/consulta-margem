import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QVBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from Consult_margem import LoginDialog as MargemDialog
from PyQt5.QtWidgets import QMessageBox


class UserLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LOGIN DE USUARIO")
        self.setFixedSize(480, 700)

        style = "border: 3px solid yellow ; border-radius:5px; padding:15px; background-color: rgb(30, 30, 30); color: white"
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        # Criação do QFrame
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: rgb(30, 30, 30);")

        self.logo = QLabel(self.frame)
        self.logo.setPixmap(QPixmap('IA/datereboot.png'))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("background-color: rgb(30, 30, 30);")

        self.user_edit = QLineEdit(self.frame)
        self.user_edit.setFixedSize(round(100.2 * 3), round(21.077 * 3))
        self.user_edit.setStyleSheet("border-radius: 4.75mm;")
        self.user_edit.setPlaceholderText("Digite seu usuário")
        self.user_edit.setStyleSheet(style)

        self.password_edit = QLineEdit(self.frame)
        self.password_edit.setFixedSize(round(100.2 * 3), round(21.077 * 3))
        self.password_edit.setStyleSheet("border-radius: 4.75mm;")
        self.password_edit.setPlaceholderText("Digite sua senha")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet(style)

        self.search_button = QPushButton('login', self.frame)
        self.search_button.setFixedSize(round(60.741 * 3), round(15.975 * 3))
        self.search_button.setStyleSheet("border-radius: 4.75mm;")
        self.search_button.setStyleSheet(style)
        self.search_button.clicked.connect(self.do_login)

        layout_v = QVBoxLayout(self.frame)
        layout_v.addWidget(self.logo, alignment=Qt.AlignCenter)
        layout_v.addWidget(self.user_edit, alignment=Qt.AlignCenter)
        layout_v.addWidget(self.password_edit, alignment=Qt.AlignCenter)
        layout_v.addWidget(self.search_button, alignment=Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.frame)

        # Conexão com o banco de dados
        self.conn = mysql.connector.connect(
            host="sql888.main-hosting.eu",
            user="u318115235_start",
            password="Vc21091992",
            database="u318115235_consulta"
        )
        self.cur = self.conn.cursor()

    def closeEvent(self, event):
        # Fechar a conexão com o banco de dados quando a janela de login for fechada
        self.conn.close()

    def do_login(self):
        # Obter o nome de usuário e senha digitados
        username = self.user_edit.text()
        password = self.password_edit.text()

        # Verificar se o usuário e senha estão corretos
        query = "SELECT * FROM user_margem WHERE username=%s AND password=%s"
        self.cur.execute(query, (username, password))
        result = self.cur.fetchone()

      

        if result:
            print("Login realizado com sucesso!")
            self.margem_dialog = MargemDialog()
            self.margem_dialog.show()
            self.accept()
        else:
            print("Usuário ou senha incorretos!")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Login inválido")
            msg_box.setText("Usuário ou senha incorretos!")
            msg_box.exec_()


            


        self.user_edit.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = UserLoginDialog()
    dialog.show()
    sys.exit(app.exec_())

    

