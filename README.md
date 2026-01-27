# K Framework Consistency Verification

This repository implements an automated pipeline to verify the consistency of K Framework definitions through Coq proof verification.

## Pipeline

1. Compile K definition to Kore intermediate representation
2. Generate Coq lemma files from Kore definition
3. Verify each lemma compiles successfully

## Usage
```bash
./run_pipeline.sh
```

## Structure

- `tree.k` - K Framework definition
- `kore_to_coq.py` - Kore to Coq converter
- `run_pipeline.sh` - Pipeline orchestration
- `.github/workflows/pipeline.yml` - CI configuration
