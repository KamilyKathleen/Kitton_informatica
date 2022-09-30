from PyQt5 import uic, QtWidgets        # Importa a interface gráfica, o formato ui do qt designer e os widgets
import mysql.connector      # Importa o conector do MySQL

conexao = mysql.connector.connect(      # Variável que armazena o conector MySQL
    host = 'localhost',     # Host do banco de dados
    user = 'root',      # Usuário do banco de dados
    password = '202173',        # Senha do banco de dados
    database = 'kitton'     # Nome do banco de dados
    )


def chama_login_func():     # Para que a janela de login de funcionários apareça:
    kitton_inicial.hide()       #  Mostra a janela inicial
    kitton_login_f.show()       # Esconde janela de login de funcionários   
    
    
def chama_produtos():       # Valida o login de funcionários e faz a janela de produtos aparecer:
    usuario = kitton_login_f.inputID.text()        # Guarda o ID
    senha_func = kitton_login_f.inputSenha.text()        # Guarda o CPF 
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados   
    # Variável que guarda o comando de seleção de dados do MySQL
    select_func = ("SELECT id, cpf FROM funcionarios WHERE id = '{}' AND cpf = '{}'".format(usuario, senha_func))  
    cursor.execute(select_func)        # Executa a variável entre parentêses
    for (id, cpf) in cursor:        # Para os valores do banco de dados na variável cursor:
        if id == usuario or cpf == senha_func:      # Se as variáveis forem iguais aos dados no banco de dados:
            kitton_login_f.hide()       # Esconde a janela de login de funcionários
            kitton_produtos.show()      # Mostra a janela de cadastro de produtos
            kitton_login_f.inputID.setText("")        # Limpa o campo
            kitton_login_f.inputSenha.setText("")        # Limpa o campo
        else:       # Senão:
            kitton_login_f.inputID.setText("Senha ou ID incorretos")        # Imprime a mensagem no campo
            kitton_login_f.inputSenha.setText("")       # Limpa o campo

            
def cad_produtos():     # Cadastra os produtos no banco de dados
    nome = kitton_produtos.inputNome.text()     # Guarda o nome
    categoria = kitton_produtos.inputCategoria.currentText()        # Guarda a categoria
    fornecedor = kitton_produtos.inputFornecedor.text()      # Guarda o fornecedor
    custo_fab = kitton_produtos.inputCustoFab.text()     # Guarda o custo de fábrica
    func = kitton_produtos.inputFucionario.currentText()       # Guarda o funcionário
    preco = kitton_produtos.inputPreco.text()        # Guarda o preço
    # Variável que guarda o comando de inserção de dados do MySQL
    inserir_prod = "INSERT INTO produtos (codigo, nome, categoria, fornecedor, custo_fabrica, funcionario, preco)values (null, %s, %s, %s, %s, %s, %s)"    
    campos = (nome, categoria, fornecedor, custo_fab, func, preco)      # Engloba todas as variáveis que o usuário digitar   
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    cursor.execute(inserir_prod, campos)        # Executa as variáveis entre parentêses
    conexao.commit()        # Comita a conexão com o banco de dados
    kitton_produtos.inputNome.setText("")     # Limpa o campo
    kitton_produtos.inputCategoria.setCurrentText("Selecione")        # Limpa o campo
    kitton_produtos.inputFornecedor.setText("")     # Limpa o campo
    kitton_produtos.inputCustoFab.setText("")     # Limpa o campo
    kitton_produtos.inputFucionario.setCurrentText("Selecione")       # Limpa o campo
    kitton_produtos.inputPreco.setText("")       # Limpa o campo
    cursor.close()      # Fecha a conexão com o banco de dados
    

def chama_cofiguracao():        # Tela de configuração
    kitton_produtos.hide()      # Esconde a tela de produtos
    kitton_configuracao.show()      # Chama a tela de configuração de produtos
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    ler = "SELECT * FROM produtos"      # Varíavel que guarda o comando select do MySQL
    cursor.execute(ler)     # Executa a variável entre parentêses
    dados = cursor.fetchall()       # Varíavel que busca/guarda todos os dados do banco de dados
    kitton_configuracao.tableWidget.setRowCount(len(dados))     # Mostra os dados do banco de dados na tabela
    kitton_configuracao.tableWidget.setRowCount(30)     # Quantidade de linhas que aparecem de cada vez
    for i in range(0, len(dados)):
        for j in range(0, 7):
            kitton_configuracao.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados[i][j])))


def pesquisa_produto():     # Pesquisar produtos pela categoria
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    pesquisa = kitton_configuracao.categoria.currentText()      # Lê o texto no campo de pesquisa
    verificar = "SELECT * FROM produtos WHERE categoria = '{}'".format(pesquisa)        # Varíavel que guarda o comando select categoria do MySQL
    cursor.execute(verificar)       # Executa a variável entre parentêses
    dados = cursor.fetchall()       # Varíavel que busca/guarda todos os dados do banco de dados
    kitton_configuracao.tableWidget.setRowCount(len(dados))     # Mostra os dados do banco de dados, de acordo com a categoria, na tabela
    kitton_configuracao.tableWidget.setRowCount(30)     # Quantidade de linhas que aparecem de cada vez
    for i in range(0, len(dados)):
        for j in range (0,7):
            kitton_configuracao.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados[i][j])))
    kitton_configuracao.categoria.setCurrentText("Selecione")       # Limpa o campo
    
    
def selecao_produto():      # Seleciona o produto através da linha selecionada
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    linha = kitton_configuracao.tableWidget.currentRow()       # Seleciona a linha da tabela
    cursor.execute("SELECT codigo FROM produtos")       # Executa o comado select codigo do MySQL
    chama_dados = cursor.fetchall()     # Varíavel que busca/guarda todos os dados do banco de dados
    valor_id = chama_dados[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE codigo = " + str(valor_id))        # Variável que guarda o comando select do MySQL
    editar = cursor.fetchall()
    kitton_configuracao.codigoPesquisa.setText(str(editar[0][0]))
    kitton_configuracao.nomeAlterar.setText(str(editar[0][1]))
    kitton_configuracao.categoriaAlterar.setCurrentText(str(editar[0][2]))
    kitton_configuracao.fornecedorAlterar.setText(str(editar[0][3]))
    kitton_configuracao.custo_fabAlterar.setText(str(editar[0][4]))
    kitton_configuracao.fucionarioAlterar.setCurrentText(str(editar[0][5]))
    kitton_configuracao.precoAlterar.setText(str(editar[0][6]))


def alter_table():      # Altera os dados do banco de dados
    codigo = kitton_configuracao.codigoPesquisa.text()      # Guarda o codigo
    nome = kitton_configuracao.nomeAlterar.text()       # Guarda/altera o nome
    categoria = kitton_configuracao.categoriaAlterar.currentText()      # Guarda/altera a categoria
    fornecedor = kitton_configuracao.fornecedorAlterar.text()       # Guarda/altera o fornecedor
    custo_fab = kitton_configuracao.custo_fabAlterar.text()     # Guarda/altera o custo dee fábrica
    funcionario = kitton_configuracao.fucionarioAlterar.currentText()       # Guarda/altera o funcionário
    preco = kitton_configuracao.precoAlterar.text()     # Guarda/altera o preço
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    # Variável que guarda o comando update do MySQL
    alterar = "UPDATE produtos SET nome = '{}', categoria = '{}', fornecedor = '{}', custo_fabrica = '{}', funcionario = '{}', preco = '{}' WHERE codigo = '{}'".format(nome, categoria, fornecedor, custo_fab, funcionario, preco, codigo)
    cursor.execute(alterar)     # Executa a variável entre parentêses
    conexao.commit()        # Comita a conexão com o banco de dados
    kitton_configuracao.codigoPesquisa.setText("")      # Limpa o campo
    kitton_configuracao.nomeAlterar.setText("")     # Limpa o campo
    kitton_configuracao.categoriaAlterar.setCurrentText("Selecione")        # Limpa o campo
    kitton_configuracao.fornecedorAlterar.setText("")       # Limpa o campo
    kitton_configuracao.custo_fabAlterar.setText("")        # Limpa o campo
    kitton_configuracao.fucionarioAlterar.setCurrentText("Selecione")       # Limpa o campo
    kitton_configuracao.precoAlterar.setText("")        # Limpa o campo
    
    
def atualizar():
    cursor = conexao.cursor()
    atualizar = "SELECT * FROM produtos"
    cursor.execute(atualizar)
    dados = cursor.fetchall()
    kitton_configuracao.tableWidget.setRowCount(len(dados))
    kitton_configuracao.tableWidget.setRowCount(30)
    for i in range(0, len(dados)):
        for j in range(0, 7):
            kitton_configuracao.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    
    
def deleta_produtos():      # Deleta um registro no banco de dados
    linha = kitton_configuracao.tableWidget.currentRow()        # Seleciona a linha da tabela
    kitton_configuracao.tableWidget.removeRow(linha)        # Remove a linha da tabela
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    cursor.execute("SELECT codigo FROM produtos")       # Executa o comado select codigo do MySQL
    dados = cursor.fetchall()       # Varíavel que busca/guarda todos os dados do banco de dados
    valor_id = dados[linha][0]      
    cursor.execute("DELETE FROM produtos WHERE codigo = " + str(valor_id))      # Executa o comado delete do MySQL
    conexao.commit()        # Comita a conexão com o banco de dados
    kitton_configuracao.codigoPesquisa.setText("")      # Limpa o campo
    kitton_configuracao.nomeAlterar.setText("")     # Limpa o campo
    kitton_configuracao.categoriaAlterar.setCurrentText("Selecione")        # Limpa o campo
    kitton_configuracao.fornecedorAlterar.setText("")       # Limpa o campo
    kitton_configuracao.custo_fabAlterar.setText("")        # Limpa o campo
    kitton_configuracao.fucionarioAlterar.setCurrentText("Selecione")       # Limpa o campo
    kitton_configuracao.precoAlterar.setText("")        # Limpa o campo
    

def chama_login_cliente():      # Para que a janela de login de clientes apareça:
    kitton_inicial.hide()       # Esconde a janela inicial
    kitton_login_c.show()       # E mostra a janela de login de clientes
    
    
def chama_cadastro():       # Para que a janela de cadastro apareça:
    kitton_login_c.hide()       # Esconde a janela de login de clientes
    kitton_cadastro.show()      # E mostra a janela de cadastro
    
    
def chama_login_2():        # Cadastra o cliente no banco de dados e volta para a janela de login de funcionários:
    cpf = kitton_cadastro.inputCPF.text()      # Guarda o CPF
    nome = kitton_cadastro.inputNome.text()     # Guarda o nome
    email = kitton_cadastro.inputEmail.text()       # Guarda o email
    nasc = kitton_cadastro.inputDataNasc.text()        # Guarda a data de nascimento
    contato = kitton_cadastro.inputContato.text()        # Guarda o contato
    cep = kitton_cadastro.inputCEP.text()        # Guarda o CEP
    rua = kitton_cadastro.inputRua.text()        # Guarda a rua
    num = kitton_cadastro.inputNumero.text()     # Guarda o número da casa
    bairro = kitton_cadastro.inputBairro.text()      # Guarda o bairro
    cidade = kitton_cadastro.inputCidade.text()      # Guarda a cidade
    uf = kitton_cadastro.inputUF.text()      # Guarda a UF do estado
    senha = kitton_cadastro.inputSenha.text()        # Guarda a senha do cliente
    # Variável que guarda o comando de inserção de dados do MySQL
    inserir_cliente = "INSERT INTO cadastro (cpf, nome, email, data_nasc, telefone, cep, rua, num_casa, bairro, cidade, uf, senha)values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    campos = (nome, cpf, email,  nasc, contato, cep, rua, num, bairro, cidade, uf, senha)      # Engloba todas as variáveis que o usuário digitar
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados
    cursor.execute(inserir_cliente, campos)     # Executa as variáveis entre parentêses
    conexao.commit()        # Comita a conexão com o banco de dados
    kitton_cadastro.inputCPF.setText("")      # Limpa o campo
    kitton_cadastro.inputNome.setText("")     # Limpa o campo
    kitton_cadastro.inputEmail.setText("")       # Limpa o campo
    kitton_cadastro.inputDataNasc.setText("")        # Limpa o campo
    kitton_cadastro.inputContato.setText("")        # Limpa o campo
    kitton_cadastro.inputCEP.setText("")        # Limpa o campo
    kitton_cadastro.inputRua.setText("")        # Limpa o campo
    kitton_cadastro.inputNumero.setText("")     # Limpa o campo
    kitton_cadastro.inputBairro.setText("")      # Limpa o campo
    kitton_cadastro.inputCidade.setText("")      # Limpa o campo
    kitton_cadastro.inputUF.setText("")      # Limpa o campo
    kitton_cadastro.inputSenha.setText("")      # Limpa o campo
    cursor.close()      # Fecha a conexão com o banco de dados
    kitton_cadastro.hide()      # Esconde a janela de cadastro
    kitton_login_c.show()       # E mostra a janela de login de clientes novamente
    
    
def chama_vendas():     # Valida o login do cliente e faz a janela de vendas aparecer:
    email = kitton_login_c.inputEmail.text()        # Guarda o email
    senha_cliente = kitton_login_c.inputSenha.text()        # Guarda a senha
    cursor = conexao.cursor()       # Função cursor, faz a conexao com o banco de dados   
    # Variável que guarda o comando de seleção de dados do MySQL
    select_cliente = ("SELECT email, senha FROM cadastro WHERE email = '{}' AND senha = '{}'".format(email, senha_cliente))
    cursor.execute(select_cliente)      # Executa a variável entre parentêses    
    for (email, senha) in cursor:       # Para os valores do banco de dados na variável cursor:
        if email == email and senha == senha_cliente:       # Se as variáveis forem iguais aos dados no banco de dados:
            kitton_login_c.hide()       # Esconde a janela de login de clientes
            kitton_vendas.show()        # E mostra a janela de vendas   
            kitton_login_c.inputEmail.setText("")        # Limpa o campo
            kitton_login_c.inputSenha.setText("")       # Limpa o campo    
        else:       # Senão:
            kitton_login_c.inputEmail.setText("Senha ou ID incorretos")        # Imprime a mensagem no campo
            kitton_login_c.inputSenha.setText("")       # Limpa o campo   


def chama_inicio_f():       # Para voltar para a janela inicial
    kitton_produtos.hide()      # Esconde a janela de produtos
    kitton_inicial.show()       # E mostra a janela inicial
    
    
def chama_inicio_c():       # Para voltar para a janela inicial
    kitton_vendas.hide()        # Esconde a janela de vendas
    kitton_inicial.show()       # E mostra a janela inicial
    
    
def chama_inicio_conf():        # Para voltar para a janela anterior
    kitton_configuracao.hide()      # Esconde a janela de configuração
    kitton_produtos.show()      # Mostra a janela de produtos
    
    
app=QtWidgets.QApplication([])      # App, Widgets e aplicações
# Links das janelas criadas no Qt Designer
kitton_inicial=uic.loadUi('kitton_inicial.ui')      # Link da janela inicial criada no QT Designer, formato .ui
kitton_login_f=uic.loadUi('kitton_login_f.ui')      # Link da janela de login de funcionários criada no QT Designer, formato .ui
kitton_produtos=uic.loadUi('kitton_produtos.ui')        # Link da janela de produtos criada no QT Designer, formato .ui
kitton_configuracao=uic.loadUi('kitton_configuração.ui')
kitton_login_c=uic.loadUi('kitton_login_c.ui')      # Link da janela de login de clientes criada no QT Designer, formato .ui
kitton_cadastro=uic.loadUi('kitton_cadastro.ui')        # Link da janela de cadastro criada no QT Designer, formato .ui
kitton_vendas=uic.loadUi('kitton_vendas.ui')        # Link da janela de vendas criada no QT Designer, formato .ui
# O que cada botão faz
kitton_inicial.botaoProdutos.clicked.connect(chama_login_func)      # Chama a tela de login do funcionário ao clicar no botão funcionário 
kitton_inicial.botaoVendas.clicked.connect(chama_login_cliente)     # Chama a tela de login do cliente ao clicar no botão cliente
kitton_login_f.botaoEntrar.clicked.connect(chama_produtos)      # Chama a tela de produtos ao clicar no botão entrar
kitton_produtos.botaoInicioFunc.clicked.connect(chama_inicio_f)       # Chama a tela de início ao clicar no botão voltar para o início
kitton_produtos.botaoCadProd.clicked.connect(cad_produtos)      # Cadastra produtos no banco de dados
kitton_produtos.botaoConfiguracao.clicked.connect(chama_cofiguracao)        # Chama a tela de configuração ao clicar no botão de engrenagem
kitton_configuracao.botaoPesquisa.clicked.connect(pesquisa_produto)     # Pesquisa o produto pela categoria ao clicar no botão de pesquisa
kitton_configuracao.botaoVoltar.clicked.connect(chama_inicio_conf)      # Volta para a tela de produtos ao clicar no botão voltar
kitton_configuracao.botaoAlterar.clicked.connect(alter_table)       # 
kitton_configuracao.botaoSelecionar.clicked.connect(selecao_produto)        # 
kitton_configuracao.botaoDeletar.clicked.connect(deleta_produtos)       # Deleta produtos do banco de dados
kitton_configuracao.botaoAtualizar.clicked.connect(atualizar)       # Atualiza a tabela com os dados do banco de dados
kitton_login_c.botaoLogar.clicked.connect(chama_vendas)     # Chama a tela de vendas ao clicar no botao logar
kitton_login_c.botaoNaoCad.clicked.connect(chama_cadastro)      # Chama a tela de cadastro ao clicar no botao ainda não possui cadastro
kitton_cadastro.botaoCadastrar.clicked.connect(chama_login_2)       # Volta para a tela de login de cliente ao clicar no botao cadastrar
kitton_vendas.botaoMenuInicial.clicked.connect(chama_inicio_c)      # Chama a tela de início ao clicar no botão menu inicial


# Inicia o aplicativo
kitton_inicial.show()       # Começa pela janela inicial
app.exec()      # Executa o aplicativo
