#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"

if [[ $# -ne 1 ]]; then
  echo "Uso: $0 <id_do_livro>" >&2
  exit 1
fi

echo "Requisição: DELETE ${API_BASE_URL}/books/$1"
echo "Resposta do endpoint:"
curl --fail-with-body --silent --show-error \
  -X DELETE "${API_BASE_URL}/books/$1" \
  --write-out 'Código HTTP: %{http_code}\n'
printf 'Livro %s excluído com sucesso.\n' "$1"

