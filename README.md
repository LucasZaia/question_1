## Como usar a API

Inicie a aplicação com:

```bash
uv run uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

Documentação:

- ReDoc: `http://127.0.0.1:8000/docs`
- Swagger UI: `http://127.0.0.1:8000/swagger`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

### Criar um livro

```bash
curl -X POST http://127.0.0.1:8000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "O Hobbit",
    "author": "J. R. R. Tolkien",
    "publication_date": "1937-09-21",
    "summary": "Um hobbit parte em uma jornada inesperada."
  }'
```

### Listar livros

```bash
curl http://127.0.0.1:8000/api/v1/books
```

### Consultar um livro por ID

```bash
curl http://127.0.0.1:8000/api/v1/books/1
```

### Pesquisar por título ou autor

A busca aceita partes do texto e não diferencia letras maiúsculas de minúsculas:

```bash
curl "http://127.0.0.1:8000/api/v1/books/search?title=Hobbit"
curl "http://127.0.0.1:8000/api/v1/books/search?author=Machado"
curl "http://127.0.0.1:8000/api/v1/books/search?title=Dom&author=Assis"
```

### Atualizar um livro

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "O Hobbit Atualizado",
    "author": "J. R. R. Tolkien",
    "publication_date": "1937-09-21",
    "summary": "Resumo atualizado do livro."
  }'
```

### Excluir um livro

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/books/1
```

A exclusão retorna `204 No Content`. A API possui um limite padrão de 100 requisições por minuto por endereço IP.

## Endpoints disponíveis

| Método | Endpoint | Descrição |
| --- | --- | --- |
| POST | `/api/v1/books` | Cria um livro |
| GET | `/api/v1/books` | Lista todos os livros |
| GET | `/api/v1/books/search` | Pesquisa por título ou autor |
| GET | `/api/v1/books/{book_id}` | Consulta um livro por ID |
| PUT | `/api/v1/books/{book_id}` | Atualiza um livro |
| DELETE | `/api/v1/books/{book_id}` | Exclui um livro |

A busca aceita partes do texto e não diferencia letras maiúsculas de minúsculas:

```text
GET /api/v1/books/search?title=Hobbit
GET /api/v1/books/search?author=Machado
GET /api/v1/books/search?title=Dom&author=Assis
```

Exemplo de dados para criação ou atualização:

```json
{
  "title": "O Pequeno Príncipe",
  "author": "J. R. R. Tolkien",
  "publication_date": "1937-09-21",
  "summary": "Um conto poético sobre amizade e responsabilidade."
}
```

## Testes

O projeto possui testes automatizados para validar os modelos, repository, service, controller, endpoints HTTP, busca por título ou autor e limite de requisições por IP.

Execute a suíte completa com:

```bash
uv run pytest
```

Os testes ajudam a garantir que alterações no código não quebrem funcionalidades existentes.

## Scripts shell

Foram criados scripts shell para facilitar o uso manual da API sem precisar montar os comandos `curl` individualmente. Eles permitem popular o banco, listar, pesquisar, criar, consultar, atualizar e excluir livros, além de executar um fluxo completo de teste dos endpoints.

Cada script exibe a requisição enviada, o corpo quando aplicável, a resposta retornada pelo controller e o código HTTP recebido.

Inicie a API antes de executar os scripts:

```bash
uv run uvicorn app.main:app --reload
```

Por padrão, os scripts usam `http://127.0.0.1:8000/api/v1`. Para apontar para outro ambiente, defina a variável `API_BASE_URL`.

### Popular o banco

Insere 20 livros de exemplo em português:

```bash
./scripts/seed_database.sh
```

### Consultar livros

```bash
# Lista todos os livros
./scripts/list_books.sh

# Pesquisa por título ou autor
./scripts/search_books.sh --title "Hobbit"
./scripts/search_books.sh --author "Machado"
./scripts/search_books.sh --title "Dom" --author "Assis"
```

Também é possível executar a busca de forma interativa. O script solicitará o título do livro ou o nome do autor:

```bash
./scripts/search_books.sh
```

### Criar um livro

Para preencher os campos no terminal, execute sem argumentos:

```bash
./scripts/create_book.sh
```

O script solicitará título, autor, data de publicação e resumo.

Para uso automatizado, informe os quatro parâmetros:

```bash
./scripts/create_book.sh \
  "O Pequeno Príncipe" \
  "Antoine de Saint-Exupéry" \
  "1943-04-06" \
  "Um conto poético sobre amizade e responsabilidade."
```

### Consultar, atualizar ou excluir por ID

```bash
./scripts/get_book.sh 1
./scripts/update_book.sh 1
./scripts/delete_book.sh 1
```

O `update_book.sh` já possui um JSON de atualização pronto dentro do script. Informe apenas o ID do livro; sem parâmetro, ele usa o ID `1`.

### Testar todos os endpoints em sequência

O script abaixo cria um livro, lista os livros, consulta pelo ID, atualiza e exclui o registro. Ele serve como um teste manual rápido do fluxo completo da API:

```bash
./scripts/run_endpoint_examples.sh
```

### Limpar todos os livros

```bash
# Solicita confirmação antes de apagar os dados
./scripts/clear_database.sh

# Execução automática sem confirmação
./scripts/clear_database.sh --yes
```

