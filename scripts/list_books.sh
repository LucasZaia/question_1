#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"

echo "Requisição: GET ${API_BASE_URL}/books"
echo "Resposta do endpoint:"
curl --fail-with-body --silent --show-error \
  "${API_BASE_URL}/books" \
  --write-out '\nCódigo HTTP: %{http_code}\n'
printf '\n'

