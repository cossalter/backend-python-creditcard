# Quick Starter

Antes de começarmos a rodar qualquer coisa, você precisará configurar algumas variáveis de ambiente para garantir o bom funcionamento. Se preferir, pode criar um arquivo `.env` na pasta `app`.

```
JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=
DATABASE_URL_CONNECTION=

```

1. **`JWT_SECRET_KEY`**: será a chave gerada pelo comando `openssl rand -hex 32`;

2. **`JWT_ALGORITHM`**: Caso tenha algum algoritmo de assinatura de token JWT preferido, esta será a variável que o seleciona. Para desenvolvimento, foi utilizado "HS256";

3. **`JWT_ACCESS_TOKEN_EXPIRE_MINUTES`**: esta variável define o tempo em que o token expirará em minutos, sendo o seu valor um número inteiro positivo;

4. **`CREDITCARD_ENCRYPT_KEY`**: será a chave gerada pelo comando `openssl rand -base64 32` e depois a string precisa ser transformando em bytes. ex: b'\<YOUR-GENERATED-KEY\>';

5. **`DATABASE_URL_CONNECTION`**: será a URL de conexão com o seu banco de dados preferido (no meu caso, utilizei o sqlite3 o tempo todo);

## Executanto

Agora podemos executar alguns comandos que estão no arquivo `Makefile`

1. **`setup-local`**: irá criar o ambiente virtual local (.venv) e instalar todas as dependências necessárias.

   **OBS**: Eu o criei utilizando o pacote [rtx](https://github.com/jdx/rtx) para gerenciar minhas versões de Python localmente.

2. **`run-local`**: facilitará nossas vidas e permitirá que rodemos a aplicação do diretório `root` do projeto.

3. **`run-tests`**: executará toda a suíte de testes desenvolvida até agora.

**OBS**: Caso não goste de criar local environment você pode executar o projeto utilizando `Docker` ou `docker-composer`.

## Curiosidade

Caso queira ver uma pseudodocumentação dos endpoints que o framework FastAPI oferece, há um endpoint dedicado para esse tipo de visualização. Basta rodar o projeto e acessar a URL http://localhost:3000/docs.
