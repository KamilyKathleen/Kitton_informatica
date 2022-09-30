from PyQt5 import uic, QtWidgets        # Importa a interface gráfica, o formato ui do qt designer e os widgets

def chama_login_func():     # Para que a janela de login de funcionários apareça:
    kitton_inicial.hide()       # Esconde a janela inicial
    kitton_login_f.show()       # E mostra a janela de login de funcionários 
    
def chama_produtos():       # Para que a janela de produtos apareça:
    kitton_login_f.hide()       # Esconde a janela de login de funcionários
    kitton_produtos.show()      # E mostra a janela de produtos
    
def chama_login_cliente():      # Para que a janela de login de clientes apareça:
    kitton_inicial.hide()       # Esconde a janela inicial
    kitton_login_c.show()       # E mostra a janela de login de clientes
    
def chama_cadastro():       # Para que a janela de cadastro apareça:
    kitton_login_c.hide()       # Esconde a janela de login de clientes
    kitton_cadastro.show()      # E mostra a janela de cadastro
    
def chama_login_2():        # Para que volte para a janela de login de funcionários:
    kitton_cadastro.hide()      # Esconde a janela de cadastro
    kitton_login_c.show()       # E mostra a janela de login de clientes novamente
    
def chama_vendas():     # Para que a janela de vendas apareça:
    kitton_login_c.hide()       # Esconde a janela de login de clientes
    kitton_vendas.show()        # E mostra a janela de vendas

def chama_inicio_f():       # Para voltar para a janela inicial
    kitton_produtos.hide()      # Esconde a janela de produtos
    kitton_inicial.show()       # E mostra a janela inicial
    
def chama_inicio_c():       # Para voltar para a janela inicial
    kitton_vendas.hide()        # Esconde a janela de vendas
    kitton_inicial.show()       # E mostra a janela inicial
    
app=QtWidgets.QApplication([])      # App, Widgets e aplicações
# Links das janelas criadas no Qt Designer
kitton_inicial=uic.loadUi('kitton_inicial.ui')      # Link da janela inicial criada no QT Designer, formato .ui
kitton_login_f=uic.loadUi('kitton_login_f.ui')      # Link da janela de login de funcionários criada no QT Designer, formato .ui
kitton_produtos=uic.loadUi('kitton_produtos.ui')        # Link da janela de produtos criada no QT Designer, formato .ui
kitton_login_c=uic.loadUi('kitton_login_c.ui')      # Link da janela de login de clientes criada no QT Designer, formato .ui
kitton_cadastro=uic.loadUi('kitton_cadastro.ui')        # Link da janela de cadastro criada no QT Designer, formato .ui
kitton_vendas=uic.loadUi('kitton_vendas.ui')        # Link da janela de vendas criada no QT Designer, formato .ui
# O que cada botão faz
kitton_inicial.botaoFunc.clicked.connect(chama_login_func)      # Chama a tela de login do funcionário ao clicar no botão funcionário 
kitton_inicial.botaoClient.clicked.connect(chama_login_cliente)     # Chama a tela de login do cliente ao clicar no botão cliente
kitton_login_f.botaoEntrar.clicked.connect(chama_produtos)      # Chama a tela de produtos ao clicar no botão entrar
kitton_produtos.botaoInicioFunc.clicked.connect(chama_inicio_f)       # Chama a tela de início ao clicar no botão voltar para o início
kitton_login_c.botaoLogar.clicked.connect(chama_vendas)     # Chama a tela de vendas ao clicar no botao logar
kitton_login_c.botaoNaoCad.clicked.connect(chama_cadastro)      # Chama a tela de cadastro ao clicar no botao ainda não possui cadastro
kitton_cadastro.botaoCadastrar.clicked.connect(chama_login_2)       # Volta para a tela de login de cliente ao clicar no botao cadastrar
kitton_vendas.botaoMenuInicial.clicked.connect(chama_inicio_c)      # Chama a tela de início ao clicar no botão menu inicial

# Inicia o aplicativo
kitton_inicial.show()       # Começa pela janela inicial
app.exec()      # Executa o aplicativo
