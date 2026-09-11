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
    conexao.execute("""
        INSERT INTO chamados
        (codigo, status, solicitante, setor, problema, data_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        chamado["id"],
        chamado["status"],
        chamado["solicitante"],
        chamado["setor"],
        chamado["problema"],
        chamado["data_hora"]
    ))

    # Salva as alterações no banco de dados
    conexao.commit()  



# Captura e formata a data e a hora do início do programa.
agora = datetime.datetime.now()
data_hora = agora.strftime("%d/%m/%Y %H:%M")

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

# Define os setores do sistema; essa tupla ainda não é usada para validar a entrada.
setores = ("TI", "RH", "Financeiro", "Administrativo")

# Define o status inicial dos chamados e o contador usado para gerar seus IDs.
status = "Em aberto"
contador = 1

# Solicita os dados do chamado, formata os textos e devolve os três valores.
def dados_chamado():

    solicitante = formatar_texto(input("Digite seu nome: "))
    setor = formatar_texto(input("Digite seu setor: "))
    problema = formatar_texto(input("Descreva o problema: "))


    return solicitante, setor, problema

# Cria um chamado com os dados recebidos e devolve seu dicionário.
def abrir_chamado(solicitante, setor, problema):

    # Permite que a função atualize o contador definido fora dela.
    global contador

    # Monta o identificador do chamado usando o contador atual.
    id_chamado = f'CALL-000{contador}'

    # Reúne os dados de um chamado em um dicionário.
    chamado = {
        "id": id_chamado,
        "status": status,
        "solicitante": solicitante,
        "setor": setor,
        "problema": problema,
        "data_hora": data_hora
        }
    
    # Prepara o contador para o próximo chamado.
    contador = contador + 1

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

                # Adiciona o chamado à lista mantida em memória.
                chamados.append(chamado)
                # Salva o chamado no banco de dados.
                salvar_chamado(chamado)

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
                encontrado = False

                # Percorre a lista inteira, colocando um dicionário por vez na variável chamado.
                for chamado in chamados:
                    # Compara o solicitante deste chamado com o nome digitado.
                    if chamado["solicitante"] == nome:
                        encontrado = True
                        # Exibe os dados somente dos chamados que correspondem ao nome.
                        print(f'ID do chamado: {chamado["id"]}')
                        print(f'Solicitante: {chamado["solicitante"]}')
                        print(f'Setor: {chamado["setor"]}')
                        print(f'Problema: {chamado["problema"]}')
                        print(f'Status: {chamado["status"]}')
                        print(f'Data e hora: {chamado["data_hora"]}')
                # Avisa quando não há nenhum chamado registrado para o nome informado.
                if not encontrado:
                    print('Usuário não encontrado.')

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
                # Avisa quando ainda não há chamados nesta execução.
                if not chamados:
                    print('Nenhum chamado cadastrado.')

                # O print fica dentro do for para exibir cada chamado da lista.
                for chamado in chamados:
                    print('==========================================')
                    print(f'             CHAMADO {chamado["id"]}')
                    print('==========================================')
                    print(f'Solicitante: {chamado["solicitante"]}')
                    print(f'Setor: {chamado["setor"]}')
                    print(f'Problema: {chamado["problema"]}')
                    print(f'Status: {chamado["status"]}')
                    print(f'Data e hora: {chamado["data_hora"]}')

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


 # 5) CONSULTA OS CHAMADOS SALVOS NO BANCO
resultado = conexao.execute("SELECT * FROM chamados")

for chamado_banco in resultado:
    print(chamado_banco)

# 6) Exibe a confirmação do chamado registrado
# print('==========================================')
#print('            CHAMADO REGISTRADO            ')
#print('==========================================') 
#print(f'ID do chamado: {chamado["id"]}')
#print(f'Solicitante: {chamado["solicitante"]}')
#print(f'Setor: {chamado["setor"]}')
#print(f'Problema: {chamado["problema"]}')
#print(f'Status: {chamado["status"]}')
#print(f'Data e hora: {chamado["data_hora"]}')

# 7) Lista todos os chamados cadastrados
#print('==========================================')
#print('          CHAMADOS CADASTRADOS            ')
#print('==========================================')
#for chamado in chamados:
#    print(f'Solicitante: {chamado["solicitante"]}')
#    print(f'Setor: {chamado["setor"]}')
#    print(f'Problema: {chamado["problema"]}')
#    print(f'Status: {chamado["status"]}')
#    print(f'Data e hora: {chamado["data_hora"]}')
#    print() 
