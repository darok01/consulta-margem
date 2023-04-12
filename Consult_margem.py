from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QTextEdit, QDesktopWidget, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from automacao import login
import sklearn
import mysql.connector
from datetime import datetime
import pandas as pd



class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.num_consultas = 0
        self.connect_database()

        self.setWindowTitle("CONSULTA DE MARGEM")

        self.setFixedSize(480, 690)

        style = "border: 2px solid yellow ; border-radius:5px; padding:15px; background-color: rgb(30, 30, 30); color: white"
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        self.logo1 = QLabel(self)
        self.logo1.setPixmap(QPixmap('IA/cosulta.png'))
        self.logo1.setFixedSize(480, 100)
        self.logo1.setAlignment(Qt.AlignCenter)
        self.logo1.setStyleSheet("background-color: rgb(30, 30, 30);")

        frame = QFrame(self)
        frame.setStyleSheet("background-color: rgb(30, 30, 30);")
        frame_layout = QVBoxLayout(frame)

        self.user_edit = QLineEdit()
        self.user_edit.setFixedSize(round(100.2 * 3), round(21.077 * 3))
        self.user_edit.setStyleSheet("border-radius: 4.75mm;")
        self.user_edit.setPlaceholderText("Digite seu usuário")
        self.user_edit.setStyleSheet(style)

        self.password_edit = QLineEdit()
        self.password_edit.setFixedSize(round(100.2 * 3), round(21.077 * 3))
        self.password_edit.setStyleSheet("border-radius: 4.75mm;")
        self.password_edit.setPlaceholderText("Digite sua senha")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet(style)

        self.select_box = QComboBox()
        self.select_box.addItem("Daycoval")
        self.select_box.addItem("Olé")
        self.select_box.addItem("Santander")
        self.select_box.setFixedSize(round(100.2 * 3), round(20.376 * 3))
        self.select_box.setStyleSheet("border-radius: 4.75mm;")
        self.select_box.setStyleSheet(style)

        self.cpf_edit = QTextEdit()
        self.cpf_edit.setFixedSize(round(100.2 * 3), round(71.376 * 3))
        self.cpf_edit.setStyleSheet("border-radius: 4.75mm;")
        self.cpf_edit.setPlaceholderText("Digite todos os CPFS")
        self.cpf_edit.setStyleSheet(style)

        self.cpf_count_label = QLabel()
        self.cpf_count_label.setStyleSheet("color: white")
        frame_layout.addWidget(self.cpf_count_label)

        self.search_button = QPushButton('Buscar')
        self.search_button.setFixedSize(round(60.741 * 3), round(15.975 * 3))
        self.search_button.setStyleSheet("border-radius: 4.75mm;")
        self.search_button.setStyleSheet(style)

        frame_layout.addWidget(self.user_edit)
        frame_layout.addWidget(self.password_edit)
        frame_layout.addWidget(self.select_box)
        frame_layout.addWidget(self.cpf_edit)
        frame_layout.addWidget(self.search_button)

        layout = QHBoxLayout()
        layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.search_button.clicked.connect(self.reconnect_database)
        self.search_button.clicked.connect(self.buscar_love)



        self.cpf_edit.textChanged.connect(self.update_cpf_count)
        
    def connect_database(self):
        self.conn = mysql.connector.connect(
            host="sql888.main-hosting.eu",
            user="u318115235_start",
            password="Vc21091992",
            database="u318115235_consulta"
        )
        self.cur = self.conn.cursor()

    def reconnect_database(self):
        self.conn.close()
        self.connect_database()
        self.delete_old_entries()
    def delete_old_entries(self):
        hoje = datetime.now().date()

        sql = "SELECT id, data FROM consultas WHERE usuario = %s"
        val = (self.user_edit.text(),)
        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        if result:
            consulta_id, data_ultima_consulta = result
            if data_ultima_consulta < hoje:
                sql = "DELETE FROM consultas WHERE id = %s"
                val = (consulta_id,)
                self.cur.execute(sql, val)
                self.conn.commit()

    def buscar_love(self):
        usuario = self.user_edit.text()
        senha = self.password_edit.text()
        banco = self.select_box.currentText()
        cpfs = self.cpf_edit.toPlainText().strip().split('\n')
        self.num_consultas += 1

        hoje = datetime.now().date()

    # Verifica se já existe uma entrada para o usuário e a data atual
        sql = "SELECT id, num_cpfs FROM consultas WHERE usuario = %s AND data = %s"
        val = (usuario, hoje)
        self.cur.execute(sql, val)
        result = self.cur.fetchone()

        if result:
        # Se existir, atualize a quantidade de CPFs na mesma linha
            consulta_id, cpf_consultados_hoje = result
            cpf_consultados_hoje += len(cpfs)

        # Verifica se o limite de 300 consultas diárias foi excedido
            if cpf_consultados_hoje > 300:
                max_cpfs = 300 - (cpf_consultados_hoje - len(cpfs))
                self.cpf_count_label.setText(f"Limite de 300 consultas diárias atingido. Você pode consultar apenas {max_cpfs} CPFs.")
                return
            else:
                self.cpf_count_label.setText(f"Usuário {usuario} já consultou {cpf_consultados_hoje} CPFs hoje.")

            sql = "UPDATE consultas SET num_cpfs = %s WHERE id = %s"
            val = (cpf_consultados_hoje, consulta_id)
        else:
        # Se não, insira uma nova linha com a quantidade de CPFs da consulta atual
            cpf_consultados_hoje = len(cpfs)

        # Verifica se o limite de 300 consultas diárias foi excedido
            if cpf_consultados_hoje > 300:
                max_cpfs = 300
                self.cpf_count_label.setText(f"Limite de 300 consultas diárias atingido. Você pode consultar apenas {max_cpfs} CPFs.")
                return

            sql = "INSERT INTO consultas (usuario, data, num_cpfs) VALUES (%s, %s, %s)"
            val = (usuario, hoje, cpf_consultados_hoje)

        self.cur.execute(sql, val)
        self.conn.commit()

        login_form = {
            "usuario": usuario,
            "senha": senha,
            "banco": banco,
            "cpf": cpfs}
        login(login_form["usuario"], login_form["senha"], login_form["banco"], login_form["cpf"])

        self.cpf_edit.clear()
        self.update_cpf_count()

        

        if cpf_consultados_hoje > 0:
            msg = f"Usuário {usuario} já consultou {cpf_consultados_hoje} CPFs hoje."
            self.cpf_count_label.setText(msg)







    def update_cpf_count(self):
        cpfs = self.cpf_edit.toPlainText().strip().split('\n')
        cpf_count = len(cpfs)
        self.cpf_count_label.setText(f"Quantidade de CPFs: {cpf_count}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())