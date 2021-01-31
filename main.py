from PyQt5 import uic, QtWidgets
import pymysql
from configdb import host, user, password, database

# conecta no banco
try:
    db = pymysql.connect(db=database, user=user, passwd=password, host=host)
    print('Conectado')
except:
    print('Erro ao conectar')

# cadastra o produto no banco
def cadastrar():
    codigo = formulario.codigo.text()
    descricao = formulario.descricao.text()
    preco = round(float((formulario.preco.text()).replace(',', '.')), 2)
    categoria = ''

    if formulario.informatica.isChecked():
        categoria = 'informatica'
    elif formulario.smartphones.isChecked():
        categoria = 'smartphones'
    elif formulario.televisores.isChecked():
        categoria = 'televisores'
    try:
        cursor = db.cursor()
        sql = "INSERT INTO produtos (codigo, descricao,preco,categoria) values (%s,%s,%s,%s)"
        dados = (str(codigo), str(descricao), str(preco), categoria)
        cursor.execute(sql, dados)
        db.commit()
        print('Cadastrado')
        formulario.codigo.setText("")
        formulario.descricao.setText("")
        formulario.preco.setText("")
    except:
        print('Erro ao cadastrar')

# lista os produtos cadastrados no banco
def listar():
    listagem.show()
    cursor = db.cursor()
    sql = "SELECT * FROM produtos"
    cursor.execute(sql)
    dados_lidos = cursor.fetchall()

    listagem.dadostabela.setRowCount(len(dados_lidos))
    listagem.dadostabela.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            listagem.dadostabela.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

# deleta o produto selecionado do banco
def delete():
    linha = listagem.dadostabela.currentRow()
    listagem.dadostabela.removeRow(linha)
    cursor = db.cursor()
    try:
        sql = "SELECT id FROM produtos"
        cursor.execute(sql)
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][0]
    except:
        if dados_lidos == ():
            print('Não há dados')
        else:
            print('Falha ao ler os dados')
    if dados_lidos != ():
        try:
            cursor.execute("DELETE FROM produtos WHERE id = " + str(valor_id))
            print('Dado excluído')
        except:
            print('Falha ao excluir o registro')

app = QtWidgets.QApplication([])
formulario = uic.loadUi("interfaces/interface.ui")
listagem = uic.loadUi("interfaces/listagem.ui")
formulario.enviarbtn.clicked.connect(cadastrar)
formulario.listarbtn.clicked.connect(listar)
listagem.excluir.clicked.connect(delete)
formulario.show()
app.exec()

# escreve as mudanças no banco e fecha a conexão
try:
    db.commit()
    db.close()
    print('Conexão finalizada')
except:
    print('Falha ao finalizar a conexão')