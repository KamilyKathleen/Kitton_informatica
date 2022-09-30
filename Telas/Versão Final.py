from PyQt5 import uic, QtWidgets        # Importa a interface gráfica
import mysql.connector      # Importa o conector do MySQL
import sys 
from cx_Freeze import setup, Executable

conexao = mysql.connector.connect(      # variável que armazena o conector do MySql
    host = 'localhost',     # Host da database
    user = 'root',      # Usuário da database
    password = '202173',        # Senha da database
    database = 'kitton'     # Nome da database
)


def chama_inicial():    # Válida o login e chama a tela inicial
    usuario = kitton_login_f.inputID.text()     # Guarda o id
    senha = kitton_login_f.inputSenha.text()    # Guarda a senha
    cursor = conexao.cursor()   # Função cursor, conecta com a database
    # Executa o comando de seleção de dados do MySQL
    cursor.execute("select id, cpf from funcionarios where id = '{}' and cpf = '{}'".format(usuario, senha))
    for id, cpf in cursor:  # Para os valores do banco de dados na variável cursor:
        if usuario == id or senha == cpf:   # Se as variáveis forem iguais aos dados no banco de dados:
            kitton_login_f.hide()   # Esconde a janela de login do funcionário
            kitton_inicial.show()   # Mostra a janela inicial
            kitton_login_f.inputID.setText("")      # Limpa o campo
            kitton_login_f.inputSenha.setText("")   # Limpa o campo
        else:   # Senão
            kitton_login_f.inputID.setText("Senha ou ID incorretos")    # Imprime a mensagem no campo
            kitton_login_f.inputSenha.setText("")   # Limpa o campo


def chama_produtos():   # Chama a tela de cadastro de produtos
    kitton_inicial.hide()   # Esconde a janela inicial
    kitton_produtos.show()  # Mostra a janela de cadastro de produtos
    
    
def cad_produtos(): # Cadastra os produtos na database
    nome = kitton_produtos.inputNome.text() # Guarda o nome
    categoria = kitton_produtos.inputCategoria.currentText()    # Guarda a categoria
    fornecedor = kitton_produtos.inputFornecedor.text() # Guarda o fornecedor
    custo_fab = kitton_produtos.inputCustoFab.text()    # Guarda o custo de fábrica
    func = kitton_produtos.inputFuncionario.currentText()    # Guarda o funcionário
    preco = kitton_produtos.inputPreco.text()   # Guarda o preço
    # Variável que guarda o comando de inserção de dados do MySQL
    inserir_prod = "insert into produtos (codigo, nome, categoria, fornecedor, custo_fabrica, funcionario, preco)values (null, %s, %s, %s, %s, %s, %s)"
    campos = (nome, categoria, fornecedor, custo_fab, func, preco)  # Guarda as variáveis entre parênteses
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    cursor.execute(inserir_prod, campos)    # Executa as variáveis entre parênteses
    conexao.commit()    # Comita a conexão com o banco de dados
    kitton_produtos.inputNome.setText("")   # Limpa o campo
    kitton_produtos.inputCategoria.setCurrentText("Selecione")  # Limpa o campo
    kitton_produtos.inputFornecedor.setText("") # Limpa o campo
    kitton_produtos.inputCustoFab.setText("")   # Limpa o campo
    kitton_produtos.inputFuncionario.setCurrentText("Selecione") # Limpa o campo
    kitton_produtos.inputPreco.setText("")  # Limpa o campo
    cursor.close()  # Fecha a conexão com o banco de dados
      
    
def chama_configuração():   # Chama a tela de gerenciamento de produtos
    kitton_produtos.hide()  # Esconde a janela de cadastro de produtos
    kitton_configuracao.show()  # Mostra a janela de gerenciamento de produtos
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    #Executa o comando select do MySQL
    cursor.execute("select * from produtos")
    dados = cursor.fetchall()   # Varíavel que busca/guarda todos os dados da database
    kitton_configuracao.tableWidget.setRowCount(len(dados)) # Mostra os dados da database na tabela
    kitton_configuracao.tableWidget.setRowCount(25)  # Quantidade de linhas que aparecem de cada vez
    for i in range(0, len(dados)):
        for j in range(0, 7):
            kitton_configuracao.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    
    
def pesquisa_categoria():   # Pesquisa produtos pela categoria 
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    pesquisa = kitton_configuracao.categoria.currentText()  # Lê o texto da caixa de seleção
    # Executa o comando select do MySQL
    cursor.execute("select * from produtos where categoria = '{}'".format(pesquisa))
    dados = cursor.fetchall()   # Variável que busca/guarda todos os dados da database
    kitton_configuracao.tableWidget.setRowCount(len(dados)) # Mostra os produtos de acordo com a categoria
    kitton_configuracao.tableWidget.setRowCount(25)  # Quantidade de linhas que aparecem por vez
    for i in range(0, len(dados)):
        for j in range(0, 7):
            kitton_configuracao.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    kitton_configuracao.categoria.setCurrentText("Selecione")   # Limpa o campo
    
    
def altera_produtos():  # Altera os produtos da database
    codigo = kitton_configuracao.codigoPesquisa.text()  # Guarda o codigo
    nome = kitton_configuracao.nomeAlterar.text()   # Guarda/altera o nome
    categoria = kitton_configuracao.categoriaAlterar.currentText()  # Guarda/altera a categoria
    fornecedor = kitton_configuracao.fornecedorAlterar.text()   # Guarda/altera o fornecedor
    custo_fab = kitton_configuracao.custo_fabAlterar.text() # Guarda/altera o custo de fábrica
    funcionario = kitton_configuracao.funcionarioAlterar.currentText()   # Guarda/altera o funcionário
    preco = kitton_configuracao.precoAlterar.text() # Guarda/altera o preço
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    # Executa o comando update do MySQL
    cursor.execute("update produtos set nome = '{}', categoria = '{}', fornecedor = '{}', custo_fabrica = '{}', funcionario = '{}', preco = '{}' where codigo = '{}'".format(nome, categoria, fornecedor, custo_fab, funcionario, preco, codigo))
    conexao.commit()    # Comita a conexão com a database
    kitton_configuracao.codigoPesquisa.setText("")  # Limpa o campo
    kitton_configuracao.nomeAlterar.setText("") # Limpa o campo
    kitton_configuracao.categoriaAlterar.setCurrentText("Selecione")    # Limpa o campo
    kitton_configuracao.fornecedorAlterar.setText("")   # Limpa o campo
    kitton_configuracao.custo_fabAlterar.setText("")    # Limpa o campo
    kitton_configuracao.funcionarioAlterar.setCurrentText("Selecione")   # Limpa o campo
    kitton_configuracao.precoAlterar.setText("")    # Limpa o campo
    

def atualizar():    # Atualiza os dados na tela de gerenciamento de produtos
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    # Executa o comando select do MySQL
    cursor.execute("select * from produtos")
    dados = cursor.fetchall()   # Variável que busca/guarda todos os dados da database
    kitton_configuracao.tableWidget.setRowCount(len(dados))  # Mostra os dados da database na tabela
    kitton_configuracao.tableWidget.setRowCount(25)    # Quantidade de linhas que aparecem por vez
    for i in range(0, len(dados)):
        for j in range(0, 7):
            kitton_configuracao.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
            

def selecao_produto():
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    linha = kitton_configuracao.tableWidget.currentRow()    # Seleciona a linha da tabela
    cursor.execute("select codigo from produtos")   # Executa o comando select codigo do MySQL
    dados = cursor.fetchall()   # Variável que busca/guarda todos os dados da database
    valor_cod = dados[linha][0]
    cursor.execute("select * from produtos where codigo = '{}'".format(str(valor_cod)))
    selecionar = cursor.fetchall()
    kitton_configuracao.codigoPesquisa.setText(str(selecionar[0][0]))
    kitton_configuracao.nomeAlterar.setText(str(selecionar[0][1]))
    kitton_configuracao.categoriaAlterar.setCurrentText(str(selecionar[0][2]))
    kitton_configuracao.fornecedorAlterar.setText(str(selecionar[0][3]))
    kitton_configuracao.custo_fabAlterar.setText(str(selecionar[0][4]))
    kitton_configuracao.funcionarioAlterar.setCurrentText(str(selecionar[0][5]))
    kitton_configuracao.precoAlterar.setText(str(selecionar[0][6]))


def deleta_produtos():  # Deleta um registro na database
    linha = kitton_configuracao.tableWidget.currentRow()    # Seleciona a linha da tabela
    kitton_configuracao.tableWidget.removeRow(linha)    # Remove a linha da tabela
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    cursor.execute("select codigo from produtos")   # Executa o comando select codigo do MySQL
    dados = cursor.fetchall()   # Variável que busca/guarda todos os dados da database
    valor_cod = dados[linha][0]
    cursor.execute("delete from produtos where codigo = '{}'".format(str(valor_cod))) # Executa o comando delete do MySQL
    conexao.commit()    # Comita a conexão com a database
    kitton_configuracao.codigoPesquisa.setText("")  # Limpa o campo
    kitton_configuracao.nomeAlterar.setText("") # Limpa o campo
    kitton_configuracao.categoriaAlterar.setCurrentText("Selecione")    # Limpa o campo
    kitton_configuracao.fornecedorAlterar.setText("")   # Limpa o campo
    kitton_configuracao.custo_fabAlterar.setText("")    # Limpa o campo
    kitton_configuracao.funcionarioAlterar.setCurrentText("Selecione")   # Limpa o campo
    kitton_configuracao.precoAlterar.setText("")    # Limpa o campo  
    
    
def chama_vendas():  # Chama a tela de caixa
    kitton_inicial.hide()   # Esconde a janela inicial
    kitton_caixa.show()  # Mostra a janela de caixa
    
    
def pesquisa_cod():     # NÃO ESTÁ FUNCIONANDO AINDA
    cursor = conexao.cursor()   # Função cursor, faz a conexao com a database
    linha = kitton_caixa.inputCod.text()
    cursor.execute("select codigo from produtos")   # Executa o comando select codigo do MySQL
    dados = cursor.fetchall()   # Variável que busca/guarda todos os dados da database
    valor_cod = dados[linha][0]
    cursor.execute("select nome, preco from produtos where codigo = '{}'".format(str(valor_cod)))
    selecionar = cursor.fetchall()
    kitton_caixa.inputCod.setText(str(selecionar[0][0]))
    kitton_caixa.inputNome.setText(str(selecionar[0][1]))
    kitton_caixa.inputPreco.setText(str(selecionar[0][6]))
    
    
def volta_produtos():   # Volta para a tela de produtos (gerenciamento de produtos)
    kitton_configuracao.hide()  # Esconde a janela de gerenciamento de produtos
    kitton_produtos.show()  # Mostra a janela de cadastro de produtos
    

def volta_inicio_p():   # Volta para a tela inicial (cadastro de produtos)
    kitton_produtos.hide()  # Esconde a janela de cadastro de produtos
    kitton_inicial.show()   # Mostra a janela inicial
    

def volta_inicio_v():   # Volta para a tela inicial (caixa)
    kitton_caixa.hide()  # Esconde a janela de caixa
    kitton_inicial.show()   # Mostra a janela inicial


app = QtWidgets.QApplication([])    # App, widgets e aplicações
# Links das janelas criadas no Qt Designer
kitton_login_f = uic.loadUi('kitton_login_f.ui')    # Janela de login do funcionário
kitton_inicial = uic.loadUi('kitton_inicial.ui')    # Janela incial
kitton_produtos = uic.loadUi('kitton_produtos.ui')  # Janela de cadastro de produtos
kitton_configuracao = uic.loadUi('kitton_configuração.ui')  # Janela de gerenciamento de cadastro de produtos
kitton_cadastro_c = uic.loadUi('kitton_cadastro.ui')    # Janela de cadastro de clientes
kitton_caixa = uic.loadUi('kitton_caixa.ui')    # Janela de caixa
# O que cada botão faz
kitton_login_f.botaoEntrar.clicked.connect(chama_inicial)   # Abre a janela inicial ao clicar no botão entrar
kitton_inicial.botaoProdutos.clicked.connect(chama_produtos)    # Abre a janela de cadastro de produtos
kitton_produtos.botaoCadProd.clicked.connect(cad_produtos)  # Cadastra os produtos na database
kitton_produtos.botaoConfiguracao.clicked.connect(chama_configuração)   # Abre a janela de gerenciamento de produtos
kitton_configuracao.botaoPesquisa.clicked.connect(pesquisa_categoria)   # Pesquisa os produtos a partir da categoria
kitton_configuracao.botaoAlterar.clicked.connect(altera_produtos)   # Altera os produtos no banco de dados
kitton_configuracao.botaoAtualizar.clicked.connect(atualizar)   # Atualiza os dados na janela de gerenciamento de produtos
kitton_configuracao.botaoSelecionar.clicked.connect(selecao_produto)    # Seleciona um produto na tabela
kitton_configuracao.botaoDeletar.clicked.connect(deleta_produtos)   # Deleta produtos da database
kitton_configuracao.botaoVoltar.clicked.connect(volta_produtos)     # Volta para a janela de cadastro de produtos
kitton_produtos.botaoInicioP.clicked.connect(volta_inicio_p)    # Volta para a janela inicial
kitton_inicial.botaoVendas.clicked.connect(chama_vendas)    # Abre a janela de caixa
kitton_caixa.botaoVoltar.clicked.connect(volta_inicio_v)    # Volta para a janela inicial
kitton_caixa.botaoPesquisar.clicked.connect(pesquisa_cod)


# Inicia o aplicativo
kitton_login_f.show()   # Começa pela janela de login do funcionário
app.exec()      # Executa o aplicativo
