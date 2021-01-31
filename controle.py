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

def cadastrar():
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

def listar():
    listagem.show()
    cursor = db.cursor()
    sql =  "SELECT * FROM produtos"
    cursor.execute(sql)
    dados_lidos = cursor.fetchall()

    listagem.dadostabela.setRowCount(len(dados_lidos))
    listagem.dadostabela.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            listagem.dadostabela.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



app = QtWidgets.QApplication([])
formulario = uic.loadUi("interface.ui")
listagem = uic.loadUi("listagem.ui")
formulario.enviarbtn.clicked.connect(cadastrar)
formulario.listarbtn.clicked.connect(listar)

formulario.show()
app.exec()