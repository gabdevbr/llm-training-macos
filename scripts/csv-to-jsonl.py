#!/usr/bin/env python3
"""
Converte CSV para JSONL format pra treinar.

Uso:
    python3 csv-to-jsonl.py input.csv output.jsonl

CSV esperado:
    instruction,response
    "Como faço X?","Faça Y então Z"
"""

import csv
import json
import sys
from pathlib import Path


def csv_to_jsonl(csv_path: str, output_path: str):
    """Converte CSV pra JSONL"""
    
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        sys.exit(1)
    
    count = 0
    with open(csv_file, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Valida header
        if not reader.fieldnames or 'instruction' not in reader.fieldnames:
            print("❌ CSV precisa ter coluna 'instruction'")
            sys.exit(1)
        
        if 'response' not in reader.fieldnames:
            print("❌ CSV precisa ter coluna 'response'")
            sys.exit(1)
        
        for row in reader:
            instruction = row.get('instruction', '').strip()
            response = row.get('response', '').strip()
            
            if not instruction or not response:
                print(f"⚠️  Pulando linha vazia: {row}")
                continue
            
            record = {
                "instruction": instruction,
                "response": response
            }
            
            outfile.write(json.dumps(record, ensure_ascii=False) + '\n')
            count += 1
    
    print(f"✅ Convertido com sucesso!")
    print(f"   {count} linhas")
    print(f"   Salvo em: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 csv-to-jsonl.py <input.csv> <output.jsonl>")
        sys.exit(1)
    
    csv_to_jsonl(sys.argv[1], sys.argv[2])
