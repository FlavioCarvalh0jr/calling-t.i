# Importa a biblioteca usada para obter a data e a hora.
import datetime
import sqlite3

# CONEXÃO COM O BANCO DE DADOS
conexao = sqlite3.connect("calling.db")

# CRIAÇÃO DA TABELA DE CHAMADOS
conexao.execute("""
    CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        status TEXT,
        solicitante TEXT,
        setor TEXT,
        problema TEXT,
        data_hora TEXT
    )
""")


# 4) SALVAR CHAMADO NO BANCO
def salvar_chamado(chamado):
    # A transacao salva o registro e seu codigo juntos.
    with conexao:
        resultado = conexao.execute("""
            INSERT INTO chamados
            (status, solicitante, setor, problema, data_hora)
            VALUES (?, ?, ?, ?, ?)
        """, (
            chamado["status"],
            chamado["solicitante"],
            chamado["setor"],
            chamado["problema"],
            chamado["data_hora"]
        ))

        # lastrowid e o ID gerado pelo SQLite para este registro.
        codigo = f"CALL-{resultado.lastrowid:04d}"
        conexao.execute(
            "UPDATE chamados SET codigo = ? WHERE id = ?",
            (codigo, resultado.lastrowid)
        )

    # Atualiza o dicionario somente depois de confirmar a gravacao.
    chamado["id"] = codigo

# 5) BUSCAR CHAMADOS NO BANCO
def buscar_chamados():
    resultado = conexao.execute("""
        SELECT codigo, status, solicitante, setor, problema, data_hora
        FROM chamados
    """)

    return resultado.fetchall()    


# Busca somente os chamados do solicitante informado.
def buscar_chamados_por_solicitante(nome):
    resultado = conexao.execute("""
        SELECT codigo, status, solicitante, setor, problema, data_hora
        FROM chamados
        WHERE solicitante = ?
    """, (nome,))

    return resultado.fetchall()


# calling t.i
# Sistema de gerenciamento de chamados de TI
# Desenvolvido como projeto de estudo em Python

# Exibe a apresentação do sistema e a mensagem de boas-vindas.
print('==========================================')
print('               CALLING T.I                ')
print('          Sistema de Chamados de TI       ')
print('==========================================')
print()
print('               Bem-vindo!                 ')
print(' sistema de gerenciamento de chamados técnicos.')
print('              Versão: 0.1                 ')

# Remove espaços das extremidades do texto e converte as letras para minúsculas.
def formatar_texto(texto):
    return texto.strip().lower()


# Define o status inicial dos chamados.
status = "Em aberto"

# Repete a pergunta até receber um texto preenchido.
def ler_campo_obrigatorio(pergunta):
    while True:
        texto = formatar_texto(input(pergunta))
        if texto:
            return texto
        print('Este campo é obrigatório. Digite um valor para continuar.')


# Solicita e valida os três campos antes de criar o chamado.
def dados_chamado():
    solicitante = ler_campo_obrigatorio("Digite seu nome: ")
    setor = ler_campo_obrigatorio("Digite seu setor: ")
    problema = ler_campo_obrigatorio("Descreva o problema: ")

    return solicitante, setor, problema


# Cria um chamado com os dados recebidos e devolve seu dicionário.
def abrir_chamado(solicitante, setor, problema):
    # Captura a data e a hora a cada novo chamado.
    agora = datetime.datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M")

    # Reúne os dados de um chamado em um dicionário.
    chamado = {
        "status": status,
        "solicitante": solicitante,
        "setor": setor,
        "problema": problema,
        "data_hora": data_hora
        }
    
    return chamado 

# Cria a lista que guarda os chamados durante a execução do programa.
chamados = []

# Repete o menu principal até que o usuário escolha sair.
while True:

    # Exibe as opções do menu principal.
    print('==========================================')
    print('              MENU PRINCIPAL              ')
    print('==========================================')
    print('1 - Usuário')
    print('2 - Técnico')
    print('3 - Sair')

    # Lê a opção escolhida no menu principal.
    opcao = input('Escolha uma opção: ')

    # Abre o menu do usuário quando a opção 1 é escolhida.
    if opcao == '1':

        # Mantém o usuário neste menu até que ele escolha voltar.
        while True:

            # Exibe as opções disponíveis para o usuário.
            print('==========================================')
            print('              MENU DO USUÁRIO             ')
            print('==========================================')
            print('1 - Abrir chamado')
            print('2 - Meus chamados')
            print('3 - Voltar')

            # Lê a opção escolhida no menu do usuário.
            opcao_usuario = input('Escolha uma opção: ')

            # Inicia o cadastro de um novo chamado.
            if opcao_usuario == '1':

                # Coleta o nome do solicitante, o setor e a descrição do problema.
                solicitante, setor, problema = dados_chamado()

                # Cria o dicionário do chamado com os dados coletados.
                chamado = abrir_chamado(solicitante, setor, problema)

                # Salva e recebe o codigo gerado a partir do ID do SQLite.
                salvar_chamado(chamado)
                chamados.append(chamado)

                # Exibe a confirmação do cadastro e os dados do chamado criado.
                print('==========================================')
                print('            CHAMADO REGISTRADO            ')
                print('==========================================')
                print(f'ID do chamado: {chamado["id"]}')
                print(f'Solicitante: {chamado["solicitante"]}')
                print(f'Setor: {chamado["setor"]}')
                print(f'Problema: {chamado["problema"]}')
                print(f'Status: {chamado["status"]}')
                print(f'Data e hora: {chamado["data_hora"]}')

            # Busca e exibe os chamados cujo solicitante tem o nome informado.
            elif opcao_usuario == '2':
                # Formata o nome da mesma maneira usada no cadastro para comparar os textos.
                nome = formatar_texto(input('Digite seu nome: '))
                # Consulta o SQLite, incluindo chamados de execuções anteriores.
                chamados_usuario = buscar_chamados_por_solicitante(nome)

                # A consulta retorna tuplas na mesma ordem das colunas do SELECT.
                for chamado in chamados_usuario:
                    codigo, status_chamado, solicitante, setor, problema, data_chamado = chamado
                    print(f'ID do chamado: {codigo}')
                    print(f'Solicitante: {solicitante}')
                    print(f'Setor: {setor}')
                    print(f'Problema: {problema}')
                    print(f'Status: {status_chamado}')
                    print(f'Data e hora: {data_chamado}')

                if not chamados_usuario:
                    print('Nenhum chamado encontrado para este solicitante.')

            # Encerra o laço do menu do usuário e retorna ao menu principal.
            elif opcao_usuario == '3':
                break

            # Avisa quando a opção não corresponde a nenhuma opção do menu do usuário.
            else:
                print('Opção inválida!')

    # Abre o menu do técnico para consultar os chamados cadastrados.
    elif opcao == '2':

        while True:
            print('==========================================')
            print('              MENU DO TÉCNICO             ')
            print('==========================================')
            print('1 - Ver chamados')
            print('2 - Voltar')

            opcao_tecnico = input('Escolha uma opção: ')

            if opcao_tecnico == '1':
                chamados_banco = buscar_chamados()

                if not chamados_banco:
                    print('Nenhum chamado cadastrado.')

                # A consulta retorna tuplas na mesma ordem das colunas do SELECT.
                for chamado in chamados_banco:
                    codigo, status_chamado, solicitante, setor, problema, data_chamado = chamado
                    print('==========================================')
                    print(f'             CHAMADO {codigo}')
                    print('==========================================')
                    print(f'Solicitante: {solicitante}')
                    print(f'Setor: {setor}')
                    print(f'Problema: {problema}')
                    print(f'Status: {status_chamado}')
                    print(f'Data e hora: {data_chamado}')

            # Encerra o laço do técnico e retorna ao menu principal.
            elif opcao_tecnico == '2':
                break

            else:
                print('Opção inválida!')

    # Exibe a mensagem de saída e encerra o laço principal.
    elif opcao == '3':
        print('Encerrando o Calling T.I...')
        break

    # Avisa quando a opção não corresponde a nenhuma opção do menu principal.
    else:
        print('Opção inválida!')
