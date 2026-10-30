#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"
BOOK_ID="${1:-1}"
UPDATE_JSON='{"title":"Livro Atualizado","author":"Autor Atualizado","publication_date":"2024-01-01","summary":"Resumo atualizado pelo script de atualização."}'

if [[ $# -gt 1 ]]; then
  echo "Uso: $0 [id_do_livro]" >&2
  exit 1
fi

echo "Requisição: PUT ${API_BASE_URL}/books/${BOOK_ID}"
echo "Corpo enviado: ${UPDATE_JSON}"
echo "Resposta do endpoint:"
curl --fail-with-body --silent --show-error \
  -X PUT "${API_BASE_URL}/books/${BOOK_ID}" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_JSON" \
  --write-out '\nCódigo HTTP: %{http_code}\n'
printf '\n'

