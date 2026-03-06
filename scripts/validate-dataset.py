#!/usr/bin/env python3
"""
Valida se dataset.jsonl tá bem formatado e completo.

Uso:
    python3 validate-dataset.py dataset.jsonl
"""

import json
import sys
from pathlib import Path


def validate_dataset(jsonl_path: str):
    """Valida dataset JSONL"""
    
    jsonl_file = Path(jsonl_path)
    if not jsonl_file.exists():
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
        sys.exit(1)
    
    errors = 0
    warnings = 0
    total = 0
    
    print(f"🔍 Validando: {jsonl_path}\n")
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total += 1
            
            # Parse JSON
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"❌ Linha {line_num}: JSON inválido - {e}")
                errors += 1
                continue
            
            # Validar estrutura
            if 'instruction' not in record:
                print(f"❌ Linha {line_num}: Falta campo 'instruction'")
                errors += 1
            
            if 'response' not in record:
                print(f"❌ Linha {line_num}: Falta campo 'response'")
                errors += 1
            
            # Validar conteúdo
            instruction = record.get('instruction', '')
            response = record.get('response', '')
            
            if not instruction or not instruction.strip():
                print(f"⚠️  Linha {line_num}: instruction vazio")
                warnings += 1
            
            if not response or not response.strip():
                print(f"⚠️  Linha {line_num}: response vazio")
                warnings += 1
            
            # Avisos de tamanho
            if len(instruction) < 5:
                print(f"⚠️  Linha {line_num}: instruction muito curto (<5 chars)")
                warnings += 1
            
            if len(response) < 10:
                print(f"⚠️  Linha {line_num}: response muito curto (<10 chars)")
                warnings += 1
    
    # Resumo
    print(f"\n{'='*50}")
    print(f"📊 Resultado:")
    print(f"   Total: {total} linhas")
    print(f"   ❌ Erros: {errors}")
    print(f"   ⚠️  Avisos: {warnings}")
    
    if errors > 0:
        print(f"\n❌ Dataset inválido. Corrija os erros acima.")
        sys.exit(1)
    elif total < 50:
        print(f"\n⚠️  Dataset pequeno ({total} linhas). Mínimo recomendado: 50+")
    elif total < 100:
        print(f"\n✅ Dataset OK, mas poderia ter mais exemplos (100+ é ideal)")
    else:
        print(f"\n✅ Dataset excelente!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 validate-dataset.py <dataset.jsonl>")
        sys.exit(1)
    
    validate_dataset(sys.argv[1])
