# RPG Dungeon Game

Este é um jogo de RPG em desenvolvimento que permite criar usuários e personagens, explorar dungeons, enfrentar monstros, ganhar XP, ouro, e evoluir suas habilidades e equipamentos. Atualmente, o jogo está em fase de desenvolvimento, com mais funcionalidades a serem implementadas no futuro. No momento, o foco principal é permitir que os jogadores explorem as dungeons.

## Funcionalidades

- **Autenticação**: Criação de contas e login de usuários.
- **Criação de personagens**: O usuário pode criar personagens com diferentes classes.
- **Exploração de dungeons**: O jogador pode explorar dungeons e enfrentar inimigos em combates.
- **Sistema de níveis**: O personagem pode subir de nível ao ganhar experiência (XP).
- **Loja**: O jogador pode comprar melhorias para seu personagem com o ouro obtido nas dungeons.

### Em desenvolvimento

- Modo história para progressão narrativa.
- Sistema de PvP (Player vs. Player).
- Sistema de inventário e equipamentos.
- Quests e sistema de banco.
- Mais monstros e dungeons.
  
## Instalação

### Pré-requisitos

- Python 3.10+
- Ambiente virtual recomendado

### Passos para instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/seu-usuario/rpg-dungeon-game.git
    ```

2. Acesse o diretório do projeto:

    ```bash
    cd rpg-dungeon-game
    ```

3. Crie um ambiente virtual (Recomendado):

    ```bash
    python -m venv venv
    ```

4. Ative o ambiente virtual:

    - No Windows:

        ```bash
        venv\Scripts\activate
        ```

    - No MacOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

6. Crie um arquivo `.env` na raiz e configure o nome do banco de dados:

    ```bash
    echo "DB_NAME=rpg.db" > rpg.db
    ```

7. Execute o jogo:

    ```bash
    python main.py
    ```

## Tecnologias Usadas

```yml
Python: Linguagem de programação principal.
Peewee: ORM usado para interação com o banco de dados SQLite.
Bcrypt: Biblioteca para hash de senhas e autenticação segura.
Colorama: Biblioteca para adicionar cores ao terminal.
Art: Biblioteca usada para criar arte ASCII no terminal.
Dotenv: Biblioteca para carregar variáveis de ambiente de arquivos .env.
```

## Estrutura do Projeto

```yml
/
├── auth.py          - Contém funções de login e registro de usuários.
├── character.py     - Manipula a criação e escolha de personagens.
├── config.py         - Configurações de banco de dados usando SQLite.
├── dungeon.py       - Lógica para criação e exploração de dungeons.
├── enemy.py         - Carregamento de monstros a partir de arquivos JSON.
├── game.py          - Lógica principal do jogo, incluindo escolha de modos de jogo.
├── history.py       - Placeholder para modo história (em desenvolvimento).
├── level_logic.py   - Funções para cálculo de atributos e XP.
├── lobby.py         - Placeholder para modo PvP (em desenvolvimento).
├── models.py        - Definição de todas as tabelas do banco de dados.
├── navigation.py    - Navegação entre menus principais e jogo.
└── user.py          - Manipulação de usuários e personagens.
```

## Banco de Dados

O banco de dados utilizado é o SQLite. As tabelas são criadas automaticamente com base nos modelos definidos em `models.py`.

## Contribuições
>
> [!TIP]
> Contribuições são bem-vindas!<br>
> Sinta-se à vontade para abrir issues ou pull requests.
