#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000/api/v1}"
TITLE=""
AUTHOR=""

usage() {
  echo "Uso: $0 [--title <título>] [--author <autor>]"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      [[ $# -ge 2 ]] || { usage >&2; exit 1; }
      TITLE="$2"
      shift 2
      ;;
    --author)
      [[ $# -ge 2 ]] || { usage >&2; exit 1; }
      AUTHOR="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 1
      ;;
  esac
done

if [[ $# -eq 0 && -z "$TITLE" && -z "$AUTHOR" ]]; then
  read -r -p "Digite o título do livro ou o nome do autor: " search_term
  TITLE="$search_term"
  AUTHOR="$search_term"
fi

if [[ -z "$TITLE" && -z "$AUTHOR" ]]; then
  echo "É necessário informar pelo menos um filtro: --title ou --author." >&2
  usage >&2
  exit 1
fi

curl_args=(
  --fail-with-body
  --silent
  --show-error
  --get "${API_BASE_URL}/books/search"
)

if [[ -n "$TITLE" ]]; then
  curl_args+=(--data-urlencode "title=${TITLE}")
fi

if [[ -n "$AUTHOR" ]]; then
  curl_args+=(--data-urlencode "author=${AUTHOR}")
fi

echo "Requisição: GET ${API_BASE_URL}/books/search"
echo "Filtros: título='${TITLE}', autor='${AUTHOR}'"
echo "Resposta do endpoint:"
curl "${curl_args[@]}" --write-out '\nCódigo HTTP: %{http_code}\n'
printf '\n'

