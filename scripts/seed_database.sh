#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

"${SCRIPT_DIR}/create_book.sh" \
  "O Hobbit" \
  "J. R. R. Tolkien" \
  "1937-09-21" \
  "Um hobbit parte em uma jornada inesperada."

"${SCRIPT_DIR}/create_book.sh" \
  "Orgulho e Preconceito" \
  "Jane Austen" \
  "1813-01-28" \
  "Um romance sobre costumes, família e primeiras impressões."

"${SCRIPT_DIR}/create_book.sh" \
  "Dom Casmurro" \
  "Machado de Assis" \
  "1899-01-01" \
  "Um clássico da literatura brasileira narrado por Bento Santiago."

"${SCRIPT_DIR}/create_book.sh" \
  "1984" \
  "George Orwell" \
  "1949-06-08" \
  "Um romance distópico sobre vigilância, controle e liberdade."

"${SCRIPT_DIR}/create_book.sh" \
  "Grande Sertão: Veredas" \
  "João Guimarães Rosa" \
  "1956-05-01" \
  "Uma narrativa brasileira sobre o sertão, a guerra e os conflitos humanos."

"${SCRIPT_DIR}/create_book.sh" \
  "A Hora da Estrela" \
  "Clarice Lispector" \
  "1977-10-26" \
  "A trajetória de Macabéa, uma jovem nordestina vivendo no Rio de Janeiro."

"${SCRIPT_DIR}/create_book.sh" \
  "Cem Anos de Solidão" \
  "Gabriel García Márquez" \
  "1967-05-30" \
  "A história de várias gerações da família Buendía na cidade de Macondo."

"${SCRIPT_DIR}/create_book.sh" \
  "O Alienista" \
  "Machado de Assis" \
  "1882-01-01" \
  "Uma sátira sobre ciência, loucura e os limites da normalidade."

"${SCRIPT_DIR}/create_book.sh" \
  "Vidas Secas" \
  "Graciliano Ramos" \
  "1938-01-01" \
  "A luta de uma família de retirantes contra a seca e a pobreza."

"${SCRIPT_DIR}/create_book.sh" \
  "Harry Potter e a Pedra Filosofal" \
  "J. K. Rowling" \
  "1997-06-26" \
  "Um jovem descobre o mundo da magia e inicia seus estudos em Hogwarts."

"${SCRIPT_DIR}/create_book.sh" \
  "O Cortiço" \
  "Aluísio Azevedo" \
  "1890-01-01" \
  "Um retrato naturalista da vida coletiva em uma habitação popular do Rio de Janeiro."

"${SCRIPT_DIR}/create_book.sh" \
  "Memórias Póstumas de Brás Cubas" \
  "Machado de Assis" \
  "1881-01-01" \
  "As memórias irreverentes de um narrador que escreve depois da própria morte."

"${SCRIPT_DIR}/create_book.sh" \
  "Capitães da Areia" \
  "Jorge Amado" \
  "1937-01-01" \
  "A história de um grupo de meninos em situação de rua nas ruas de Salvador."

"${SCRIPT_DIR}/create_book.sh" \
  "São Bernardo" \
  "Graciliano Ramos" \
  "1934-01-01" \
  "A trajetória de um fazendeiro ambicioso em busca de poder e reconhecimento."

"${SCRIPT_DIR}/create_book.sh" \
  "A Moreninha" \
  "Joaquim Manuel de Macedo" \
  "1844-01-01" \
  "Um romance brasileiro sobre amor, promessas e reencontros."

"${SCRIPT_DIR}/create_book.sh" \
  "Iracema" \
  "José de Alencar" \
  "1865-01-01" \
  "Uma narrativa indianista sobre amor, identidade e a formação do Ceará."

"${SCRIPT_DIR}/create_book.sh" \
  "O Quinze" \
  "Rachel de Queiroz" \
  "1930-01-01" \
  "Um romance sobre os efeitos da grande seca de 1915 no Ceará."

"${SCRIPT_DIR}/create_book.sh" \
  "Quarto de Despejo" \
  "Carolina Maria de Jesus" \
  "1960-01-01" \
  "Diário de uma mulher que registra a vida e a pobreza em uma favela de São Paulo."

"${SCRIPT_DIR}/create_book.sh" \
  "A Revolução dos Bichos" \
  "George Orwell" \
  "1945-08-17" \
  "Uma fábula política sobre poder, revolução e desigualdade."

"${SCRIPT_DIR}/create_book.sh" \
  "As Aventuras de Tom Sawyer" \
  "Mark Twain" \
  "1876-06-01" \
  "As aventuras de um garoto travesso às margens do rio Mississippi."

echo "Banco populado com sucesso."

