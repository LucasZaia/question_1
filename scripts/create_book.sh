#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"

if [[ $# -eq 0 ]]; then
  read -r -p "Digite o título do livro: " title
  read -r -p "Digite o nome do autor: " author
  read -r -p "Digite a data de publicação (AAAA-MM-DD): " publication_date
  read -r -p "Digite o resumo do livro: " summary
elif [[ $# -eq 4 ]]; then
  title="$1"
  author="$2"
  publication_date="$3"
  summary="$4"
else
  echo "Uso: $0 <título> <autor> <data_de_publicação> <resumo>" >&2
  exit 1
fi

if [[ -z "$title" || -z "$author" || -z "$publication_date" || -z "$summary" ]]; then
  echo "Todos os campos são obrigatórios." >&2
  exit 1
fi

request_body="$(printf '{"title":"%s","author":"%s","publication_date":"%s","summary":"%s"}' "$title" "$author" "$publication_date" "$summary")"
echo "Requisição: POST ${API_BASE_URL}/books"
echo "Corpo enviado: ${request_body}"
echo "Resposta do endpoint:"
curl --fail-with-body --silent --show-error \
  -X POST "${API_BASE_URL}/books" \
  -H "Content-Type: application/json" \
  -d "$request_body" \
  --write-out '\nCódigo HTTP: %{http_code}\n'
printf '\n'

