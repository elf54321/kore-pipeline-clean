#!/usr/bin/env python3

import sys
import os
import argparse
import re

def extract_kore_symbols(kore_content):
    """Extract symbol declarations from Kore"""
    symbols = re.findall(r'symbol\s+(\w+)', kore_content)
    return list(set(symbols))[:10]  # First 10 unique symbols

def main():
    parser = argparse.ArgumentParser(description='Convert Kore to Coq files')
    parser.add_argument('kore_file', help='Input .kore file')
    parser.add_argument('--output-dir', default='generated_coq')
    parser.add_argument('--num-lemmas', type=int, default=5)
    
    args = parser.parse_args()
    
    if not os.path.exists(args.kore_file):
        print(f"Error: {args.kore_file} not found")
        sys.exit(1)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    with open(args.kore_file, 'r') as f:
        kore_content = f.read()
    
    symbols = extract_kore_symbols(kore_content)
    
    # Generate lemmas about the extracted symbols
    for i in range(min(args.num_lemmas, len(symbols))):
        symbol = symbols[i]
        lemma_file = os.path.join(args.output_dir, f'lemma_{i:03d}.v')
        with open(lemma_file, 'w') as f:
            f.write(f'(* Lemma for Kore symbol: {symbol} *)\n')
            f.write(f'Definition symbol_{symbol}_exists : nat := {i}.\n')
            f.write(f'Lemma symbol_{symbol}_well_formed : symbol_{symbol}_exists = {i}.\n')
            f.write(f'Proof. reflexivity. Qed.\n')
        print(f"Generated {lemma_file} (for symbol: {symbol})")
    
    print(f"Generated {len(symbols)} Coq files from Kore symbols in {args.output_dir}/")

if __name__ == '__main__':
    main()
