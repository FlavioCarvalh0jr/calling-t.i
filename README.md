# Calling T.I.

Sistema de chamados de TI desenvolvido em **Python**, com interface no **terminal** e armazenamento em **SQLite**.

O projeto permite registrar problemas de suporte e consultar as solicitações cadastradas. Está sendo desenvolvido como parte dos meus estudos de programação, evoluindo conforme aprendo e aplico novos conceitos.

**Versão atual: 0.1 — em desenvolvimento.**

## Objetivo

Construir um sistema simples para organizar solicitações de suporte técnico, reunindo informações como solicitante, setor e descrição do problema.

Além da funcionalidade, o projeto tem um objetivo de aprendizado: praticar a construção de um fluxo completo, desde a entrada de dados até o armazenamento e a consulta no banco.

## Como funciona

```text
Usuário informa o solicitante, setor e problema
                      ↓
Sistema gera um código e define o status inicial
                      ↓
Chamado é salvo no SQLite
                      ↓
Técnico consulta os chamados registrados
```

## Funcionalidades atuais

- Navegação por menus no terminal.
- Abertura de chamados com solicitante, setor e descrição do problema.
- Geração de código único a partir do ID do SQLite.
- Definição do status inicial como “Em aberto”.
- Armazenamento dos chamados em banco SQLite.
- Consulta dos chamados salvos pela área do técnico.
- Busca pelo nome em “Meus chamados”, incluindo registros de execuções anteriores.
- Data e hora obtidas a cada abertura de chamado.
- Campos obrigatórios: nome, setor e descrição do problema.

## Demonstração

Exemplo ilustrativo de abertura de chamado no terminal:

```text
==========================================
              MENU DO USUÁRIO
==========================================
1 - Abrir chamado
2 - Meus chamados
3 - Voltar

Escolha uma opção: 1
Digite seu nome: Flavio
Digite seu setor: Administrativo
Descreva o problema: Computador não liga

==========================================
            CHAMADO REGISTRADO
==========================================
ID do chamado: CALL-0001
Solicitante: flavio
Setor: administrativo
Problema: computador não liga
Status: Em aberto
Data e hora: 14/09/2026 10:30
```

Os textos informados são convertidos para minúsculas e têm os espaços das extremidades removidos.

Na área do técnico, a opção **Ver chamados** consulta o banco e exibe os registros, incluindo chamados de execuções anteriores.

## Atualizar o status de um chamado

No menu principal, escolha **2 - Técnico** e depois **3 - Atualizar status**.
Informe o código (por exemplo, `CALL-0001`), confira o status atual e selecione:

- **1:** Em aberto.
- **2:** Em atendimento.
- **3:** Concluído.
- **0:** Cancelar sem alterar.

O sistema permite escolher qualquer um dos três status, inclusive reabrir um chamado. A mudança é salva no SQLite e aparece nas consultas de usuário e técnico. Códigos inexistentes não alteram registros; opções inválidas repetem a pergunta. Códigos duplicados antigos são recusados para evitar atualizar o chamado errado.

## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Lógica do sistema, menus e tratamento dos dados. |
| SQLite | Armazenamento e consulta dos chamados. |
| `sqlite3` | Comunicação entre Python e SQLite. |
| `datetime` | Obtenção e formatação de data e hora. |
| Git e GitHub | Versionamento e disponibilização do projeto. |

## Como executar

É necessário ter **Python 3** instalado. O programa utiliza bibliotecas que acompanham o Python, sem dependências externas.

**1. Clone o repositório:**

```bash
git clone https://github.com/FlavioCarvalh0jr/calling-t.i.git
```

**2. Acesse a pasta:**

```bash
cd calling-t.i
```

**3. Execute o programa:**

```bash
python main.py
```

No Windows, também é possível utilizar:

```bash
py main.py
```

O arquivo `calling.db` e a tabela de chamados são criados automaticamente, caso ainda não existam. O banco fica sempre ao lado de `main.py`, independentemente da pasta de onde o programa é executado.

## Organização atual

A pasta está organizada assim:

```text
CALLING T.I/
├── main.py              # Aplicação atual: execute este arquivo
├── README.md            # Apresentação e instruções
├── roadmap.md           # Etapas concluídas e planejadas
├── .gitignore           # Arquivos locais excluídos do Git
├── calling.db           # Banco local, não versionado
├── backups/             # Cópias de segurança locais, não versionadas
└── estudos/
    ├── README.md        # Orientações para os estudos
    ├── testes_main.py   # Versão antiga de estudo; não são testes automatizados
    └── exercicios       # Arquivo reservado para exercícios
```

`calling.db` e `backups/` são locais e não acompanham o clone do repositório. A aplicação continua concentrada em `main.py`; a separação em módulos será feita em outra etapa. Os arquivos de estudo foram preservados.

O caminho do banco é calculado a partir da localização de `main.py`. As cópias de segurança são manuais; o programa não cria backups automaticamente.

## Banco de dados

Os registros são armazenados na tabela `chamados`:

| Campo | Informação armazenada |
|---|---|
| `id` | Identificador numérico gerado pelo SQLite. |
| `codigo` | Código exibido ao usuário, como `CALL-0001`. |
| `status` | Situação do chamado. |
| `solicitante` | Nome informado no cadastro. |
| `setor` | Setor do solicitante. |
| `problema` | Descrição do problema. |
| `data_hora` | Data e hora em formato de texto. |

O identificador interno do banco e o código apresentado ao usuário são campos diferentes. O código é formado a partir do ID, por exemplo: ID 15 → CALL-0015. O cadastro e a gravação do código ocorrem na mesma transação.

## Decisões e aprendizados

### Persistência com SQLite

Guardar chamados apenas em uma lista limita o acesso à execução atual. O SQLite foi incorporado para preservar os registros depois que o programa é encerrado e permitir consultas posteriores.

### Organização dos dados com dicionários

Durante o cadastro, cada chamado é representado por um dicionário. Isso permite acessar os valores por nomes como `solicitante`, `setor` e `problema`.

### Padronização de textos

Uma função centraliza o uso de `strip()` e `lower()`. Dessa forma, cadastro e busca pelo nome utilizam a mesma padronização.

### Consultas com parâmetros

A função de busca por solicitante utiliza `WHERE solicitante = ?`, passando o nome separadamente da instrução SQL.

### Leitura dos resultados do banco

As consultas retornam registros em tuplas. A exibição na área do técnico utiliza a ordem das colunas do `SELECT` para identificar cada informação.

## Limitações da versão atual

- As áreas de usuário e técnico são opções de menu, sem autenticação.
- A busca usa o nome informado; pessoas com o mesmo nome não são diferenciadas.
- Ainda não há uma suíte de testes automatizados versionada.

## Próximos passos

As próximas etapas estão no [roadmap](roadmap.md), incluindo evolução do atendimento, organização do código e planejamento da versão web.

As melhorias serão realizadas gradualmente, mantendo o código compreensível e acompanhando meu avanço nos estudos.
