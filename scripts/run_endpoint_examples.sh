#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

echo "Criando um livro:"
create_response="$("${SCRIPT_DIR}/create_book.sh" \
  "Livro de Exemplo" \
  "Autor de Exemplo" \
  "2024-01-15" \
  "Um livro criado pelo script de exemplo dos endpoints.")"
printf '%s\n' "$create_response"

book_id="$(printf '%s' "$create_response" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p')"
if [[ -z "$book_id" ]]; then
  echo "Não foi possível obter o ID do livro criado na resposta da API." >&2
  exit 1
fi

echo "Listando livros:"
"${SCRIPT_DIR}/list_books.sh"

echo "Consultando o livro ${book_id}:"
"${SCRIPT_DIR}/get_book.sh" "$book_id"

echo "Atualizando o livro ${book_id}:"
"${SCRIPT_DIR}/update_book.sh" "$book_id"

echo "Excluindo o livro ${book_id}:"
"${SCRIPT_DIR}/delete_book.sh" "$book_id"

echo "Todos os exemplos de endpoints foram executados com sucesso."

