#!/bin/bash
set -e

K_FILE="tree.k"
KORE_DIR="tree-kompiled"
KORE_FILE="${KORE_DIR}/definition.kore"
COQ_DIR="generated_coq"

echo "[1/3] Compiling K definition"
[ -d "${KORE_DIR}" ] && rm -rf "${KORE_DIR}"

if ! kompile "${K_FILE}" --backend haskell 2>&1; then
    echo "Error: K compilation failed"
    exit 1
fi

[ ! -f "${KORE_FILE}" ] && echo "Error: Kore file not generated" && exit 1

echo "[2/3] Generating Coq files"
rm -rf "${COQ_DIR}"

if ! python3 kore_to_coq.py "${KORE_FILE}" --output-dir "${COQ_DIR}" --num-lemmas 5; then
    echo "Error: Coq generation failed"
    exit 1
fi

echo "[3/3] Verifying Coq lemmas"
FAILED_FILES=()
SUCCESS_COUNT=0

for coq_file in "${COQ_DIR}"/*.v; do
    [ -f "$coq_file" ] || continue
    
    if coqc "$coq_file" > "${coq_file}.log" 2>&1; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        rm -f "${coq_file}.log"
    else
        FAILED_FILES+=("$coq_file")
    fi
done

if [ ${#FAILED_FILES[@]} -eq 0 ]; then
    echo "Success: All ${SUCCESS_COUNT} lemmas verified"
    exit 0
else
    echo "Failure: ${#FAILED_FILES[@]} lemma(s) failed"
    for file in "${FAILED_FILES[@]}"; do
        echo "Failed: $(basename "$file")"
        cat "${file}.log"
    done
    exit 1
fi
