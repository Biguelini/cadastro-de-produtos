from PyQt5 import uic,QtWidgets
import mysql.connector
from configdb import host, user, password, database
try:
    db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    print('Conectado')
except:
    print('Erro ao conectar')

def main():
    codigo = formulario.codigo.text()
    descricao = formulario.descricao.text()
    preco = round(float((formulario.preco.text()).replace(',','.')),2)
    categoria = ''

    if formulario.informatica.isChecked():
        categoria = 'informatica'
    elif formulario.smartphones.isChecked():
        categoria = 'smartphones'
    elif formulario.televisores.isChecked():
        categoria = 'televisores'
    try:
        cursor = db.cursor()
        sql =  "INSERT INTO produtos (codigo, descricao,preco,categoria) values (%s,%s,%s,%s)"
        dados = (str(codigo), str(descricao), str(preco), categoria)
        cursor.execute(sql, dados)
        db.commit()
        print('Cadastrado')
        formulario.codigo.setText("")
        formulario.descricao.setText("")
        formulario.preco.setText("")
    except:
        print('Erro ao cadastrar')

app = QtWidgets.QApplication([])
formulario = uic.loadUi("interface.ui")
formulario.enviarbtn.clicked.connect(main)

formulario.show()
app.exec()