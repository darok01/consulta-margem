import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFrame
import sys
from datetime import date

class UserManagement(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerenciamento de Usuários")
        self.setFixedSize(480, 600)

        style = """
            QWidget {
                background-color: black;
            }
            QLineEdit {
                background-color: rgb(60, 60, 60);
                border-radius: 10px;
                border: 2px solid yellow;
                padding: 10px;
                color: white;
            }
            QPushButton {
                background-color: rgb(90, 90, 90);
                color: white;
                border-radius: 10px;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(120, 120, 120);
            }
        """
        self.setStyleSheet(style)

        # Conexão com o banco de dados
        self.conn = mysql.connector.connect(
            host="sql888.main-hosting.eu",
            user="u318115235_start",
            password="Vc21091992",
            database="u318115235_consulta"
        )

        # Cria um cursor para executar as consultas SQL
        self.cur = self.conn.cursor()

        # Criação dos widgets
        self.ent_username = QLineEdit()
        self.ent_username.setPlaceholderText("Digite seu nome de usuário")

        self.ent_password = QLineEdit()
        self.ent_password.setPlaceholderText("Digite sua senha")

        self.btn_create_user = QPushButton("Criar Usuário")
        self.btn_create_user.clicked.connect(self.create_user)

        # Aplica os parâmetros aos campos de entrada
        self.set_input_field_params(self.ent_username)
        self.set_input_field_params(self.ent_password)

        # Cria um quadro ao redor dos widgets e do botão "Criar Usuário"
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setLineWidth(2)

        layout = QVBoxLayout(self.frame)
        layout.addWidget(self.ent_username)
        layout.addWidget(self.ent_password)
        layout.addWidget(self.btn_create_user)

        # Define o espaçamento entre os widgets
        layout.setSpacing(20)

        # Adiciona o layout vertical do quadro ao layout vertical da janela
        layout = QVBoxLayout()
        layout.addWidget(self.frame)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def set_input_field_params(self, field):
        # Define os parâmetros do campo de entrada
        field.setFixedSize(300, 40)
        field.setStyleSheet("border-radius: 10px;")

    def check_user_validity(self, username):
        # Obtém a data de validade do usuário com base no nome de usuário
        self.cur.execute("SELECT `expiration_date` FROM `user_margem` WHERE `username`=%s", (username,))
        result = self.cur.fetchone()

        if result is None:
            # Se o usuário não for encontrado, retorna False
            return False

        # Converte a data de validade para um objeto date Python
        expiration_date = result[0]
        expiration_date = date(expiration_date.year, expiration_date.month, expiration_date.day)

        # Verifica se a data de validade é posterior ou igual à data atual
        return expiration_date >= date.today()

    def create_user(self):
                # Obtém os valores dos campos de entrada
        username = self.ent_username.text()
        password = self.ent_password.text()

        # Executa a consulta para inserir um novo usuário
        sql = "INSERT INTO user_margem (username, password, expiration_date) VALUES (%s, %s, DATE_ADD(CURDATE(), INTERVAL 30 DAY))"
        val = (username, password)
        self.cur.execute(sql, val)

        # Comita as alterações no banco de dados
        self.conn.commit()

        # Verifica se o usuário é válido
        if self.check_user_validity(username):
            # Limpa os campos de entrada
            self.ent_username.clear()
            self.ent_password.clear()

            # Exibe uma mensagem de sucesso
            QMessageBox.information(self, "Sucesso", "Usuário criado com sucesso!")
        else:
            # Se o usuário não for válido, remove o usuário recém-criado
            self.cur.execute("DELETE FROM `user_margem` WHERE `username`=%s", (username,))
            self.conn.commit()

            # Exibe uma mensagem de erro
            QMessageBox.warning(self, "Erro", "A data de validade deste usuário já expirou.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserManagement()
    window.show()
    sys.exit(app.exec_())

