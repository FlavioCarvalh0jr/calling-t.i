# calling t.i
# Sistema de gerenciamento de chamados de TI
# Desenvolvido como projeto de estudo em Python

print('==========================================')
print('               CALLING T.I                ')
print('          Sistema de Chamados de TI       ')
print('==========================================')
print()
print('               Bem-vindo!                 ')
print(' sistema de gerenciamento de chamados técnicos.')
print('              Versão: 0.1                 ')


def dados_chamado():

    solicitante = input('Digite seu nome: ')
    setor = input('Digite seu setor: ')
    problema = input('Digite o problema: ')

    return solicitante, setor, problema

solicitante, setor, problema = dados_chamado()

status = "Em aberto"
contador = 1

# criando a função abrir_chamado
def abrir_chamado(solicitante, setor, problema):

    global contador

    id_chamado = f'CALL-000{contador}'

    # 3) DICIONÁRIO (um chamado)
    chamado = {
        "id": id_chamado,
        "status": status,
        "solicitante": solicitante,
        "setor": setor,
        "problema": problema
        }
    
    contador = contador + 1

    return chamado 

# 4) LISTA (vazia)
chamados = []

chamado = abrir_chamado(solicitante, setor, problema)

# 5) Coloca o dicionário dentro da lista
chamados.append(chamado)

# 6) Exibe a confirmação do chamado registrado
print('==========================================')
print('            CHAMADO REGISTRADO            ')
print('==========================================') 
print(f'ID do chamado: {chamado["id"]}')
print(f'Solicitante: {chamado["solicitante"]}')
print(f'Setor: {chamado["setor"]}')
print(f'Problema: {chamado["problema"]}')
print(f'Status: {chamado["status"]}')

# 7) Lista todos os chamados cadastrados
print('==========================================')
print('          CHAMADOS CADASTRADOS            ')
print('==========================================')
for chamado in chamados:
    print(f'ID: {chamado["id"]}')
    print(f'Solicitante: {chamado["solicitante"]}')
    print(f'Setor: {chamado["setor"]}')
    print(f'Problema: {chamado["problema"]}')
    print(f'Status: {chamado["status"]}')
    print() 