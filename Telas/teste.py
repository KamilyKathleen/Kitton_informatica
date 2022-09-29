def selecao_dado():
   cursor=conexao.cursor()
   linha= configuracao.tableWidget.currentRow()
   cursor.execute('SELECT cod FROM cadastro_produto')
   execute_sql = cursor.fetchall()
   valor_id = execute_sql[linha][0]
   cursor.execute("SELECT * FROM cadastro_produto WHERE cod = " + str(valor_id))
   editar = cursor.fetchall()

   configuracao.cod_pro.setText(str(editar[0][0]))
   configuracao.nome_pro_alt.setText(str(editar[0][1]))
   configuracao.cat1.setCurrentText(str(editar[0][2]))
   configuracao.fornecedor_alt.setText(str(editar[0][3]))
   configuracao.custo_fab_alt.setText(str(editar[0][4]))
   configuracao.cat2.setCurrentText(str(editar[0][5]))
   configuracao.valor_ved_alt.setText(str(editar[0][6]))