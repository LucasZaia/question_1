#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATABASE_URL="${DATABASE_URL:-sqlite:///./books.db}"

if [[ "$DATABASE_URL" != sqlite:///* ]]; then
  echo "Este script suporta apenas URLs de banco SQLite." >&2
  exit 1
fi

DATABASE_PATH="${DATABASE_URL#sqlite:///}"
if [[ "$DATABASE_PATH" != /* ]]; then
  DATABASE_PATH="${PROJECT_DIR}/${DATABASE_PATH#./}"
fi

if [[ ! -f "$DATABASE_PATH" ]]; then
  echo "Arquivo do banco não encontrado: $DATABASE_PATH"
  exit 0
fi

if [[ "${1:-}" != "--yes" ]]; then
  echo "Todos os livros serão excluídos permanentemente de: $DATABASE_PATH"
  read -r -p "Digite 'EXCLUIR' para continuar: " confirmation
  if [[ "$confirmation" != "EXCLUIR" ]]; then
    echo "Operação cancelada."
    exit 0
  fi
fi

DATABASE_PATH="$DATABASE_PATH" uv run python - <<'PY'
import os
import sqlite3

database_path = os.environ["DATABASE_PATH"]
with sqlite3.connect(database_path) as connection:
    cursor = connection.execute("DELETE FROM books")
    deleted_rows = cursor.rowcount
    connection.commit()
    connection.execute("VACUUM")

print(f"{deleted_rows} livro(s) excluído(s) do banco de dados.")
PY

