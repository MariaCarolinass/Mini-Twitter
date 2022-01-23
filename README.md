
# Mini-Twitter

O Mini-Twitter é um pequeno projeto com funcionalidades básicas da rede social
Twitter. No projeto foram implementadas as funcionalidades de cadastro e
autenticação dos usuários; cadastro de postagens; e seguir usuários.

Confira os modelos do Mini-Twitter na pasta [/diagramas](https://github.com/MariaCarolinass/Mini-Twitter/tree/main/diagramas)

## Tecnologias utilizadas

- REST API
- Linguagem de programação Python
- Microframework web Flask
- Framework web Bootstrap

## Como instalar

Faça um fork do projeto! E clone o repositório do fork feito:

```sh
$ git clone https://github.com/seu-usuario/Mini-Twitter.git
$ cd Mini-Twitter
```

### Instalando o projeto

Instale o ambiente Virtualenv:

```sh
$ sudo apt-get install python3-venv
```

Crie a pasta venv para o Virtualenv:

```sh
$ python3 -m venv venv
```

Acesse o Virtualenv:

```sh
$ source venv/bin/activate       (Linux)
$ source venv\Script\activate    (Windows)
```

Instale a lista de pacotes do projeto:

```sh
$ pip install -r requirements.txt
```

### Configurando o projeto

Instale o Postgresql para o banco de dados:

```sh
sudo apt-get install postgresql postgresql-contrib
```

Crie um usuário administrador para o PostgreSQL:

```sh
sudo -u postgres createuser --superuser name_of_user
```

E por fim, crie o banco de dados:

```sh
sudo -u name_of_user createdb minitwitter
```

Acesse banco de dados e confira se funcionou:

```sh
psql -U name_of_user -d minitwitter
```

Utilize o comanado abaixo para iniciar o banco de dados do sqlalchemy:

```sh
$ flask db init
```

Salve as atualizações feitas:

```sh
$ flask db migrate -m "criando banco de dados"
```

Atualize o banco  de dados:

```sh
$ flask db upgrade
```

### Rodando o projeto

Para rodar o projeto utilize:

```sh
$ flask run
```

Entre no seu navegador e acesse o endereço abaixo:

```sh
http://localhost:5000/
```

## Documentação da API

#### Informações da API

```http
  GET /api
```

#### Faz a autenticação do usuário

```sh
  GET /
  GET /login
  Post /login
```

#### Saí do login do usuário

```sh
  GET /logout
```

#### Solicita token de autenticação

```sh
  GET /api/token
```

#### Carrega todos os dados das postagens

```sh
  GET /api/register_posts
```

#### Carrega todos os dados dos usuários

```sh
  GET /api/register_users
```

#### Mostra todas as postagens dos usuários

```sh
  GET /explore
```

#### Cadastra e exibe uma nova postagem

```sh
  GET /index
  Post /index
```

#### Cadastra um novo usuário

```sh
  GET /register
  Post /register
```

#### Segue um usuário

```sh
  GET /follow/{username}
  Post /follow/{username}
```

#### Para de seguir um usuário

```sh
  GET /unfollow/{username}
  Post /unfollow/{username}
```

### Para acessar a Documentação

```sh
$ flask run

http://127.0.0.1:5000/apidoc/swagger
http://127.0.0.1:5000/apidoc/redoc
```

## Licença do projeto

[GPL-3.0](https://github.com/MariaCarolinass/Mini-Twitter/blob/main/LICENSE).

## Contato

Telegram - [@carols0](https://t.me/carols0)
