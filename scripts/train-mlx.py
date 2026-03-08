#!/usr/bin/env python3
"""
Fine-tuning Skynet com MLX (Apple Silicon)
Usa LoRA + Llama 3.1 8B via mlx-lm

Uso: python3 train-mlx.py --dataset dataset.jsonl --epochs 3
"""

import json
import argparse
import subprocess
import os
import sys
from pathlib import Path

def convert_dataset(input_path, output_dir):
    """Converte JSONL {instruction, response} para formato mlx-lm"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_path, 'r') as f:
        lines = [json.loads(l) for l in f if l.strip()]
    
    # mlx-lm espera formato chat com messages
    train_data = []
    for ex in lines:
        train_data.append({
            "messages": [
                {"role": "user", "content": ex["instruction"]},
                {"role": "assistant", "content": ex["response"]}
            ]
        })
    
    # Split: 90% train, 10% valid
    split = int(len(train_data) * 0.9)
    
    train_file = os.path.join(output_dir, "train.jsonl")
    valid_file = os.path.join(output_dir, "valid.jsonl")
    
    with open(train_file, 'w') as f:
        for ex in train_data[:split]:
            f.write(json.dumps(ex) + '\n')
    
    with open(valid_file, 'w') as f:
        for ex in train_data[split:]:
            f.write(json.dumps(ex) + '\n')
    
    print(f"✅ Dataset convertido:")
    print(f"   Train: {split} exemplos → {train_file}")
    print(f"   Valid: {len(train_data) - split} exemplos → {valid_file}")
    
    return output_dir

def main():
    parser = argparse.ArgumentParser(description="Fine-tune Skynet com MLX (Apple Silicon)")
    parser.add_argument("--dataset", default="dataset.jsonl", help="Dataset JSONL")
    parser.add_argument("--model", default="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit", help="Modelo base")
    parser.add_argument("--epochs", type=int, default=3, help="Épocas de treino")
    parser.add_argument("--batch_size", type=int, default=2, help="Batch size")
    parser.add_argument("--lora_rank", type=int, default=16, help="LoRA rank")
    parser.add_argument("--learning_rate", type=float, default=1e-5, help="Learning rate")
    parser.add_argument("--output", default="./models/skynet-v1", help="Diretório de saída")
    parser.add_argument("--iters", type=int, default=0, help="Max iterations (0 = auto)")
    
    args = parser.parse_args()
    
    print("🤖 Fine-tuning Skynet com MLX (Apple Silicon)")
    print(f"   Modelo: {args.model}")
    print(f"   Dataset: {args.dataset}")
    print(f"   Épocas: {args.epochs}")
    print(f"   Batch: {args.batch_size}")
    print(f"   LoRA rank: {args.lora_rank}")
    print(f"   LR: {args.learning_rate}")
    print(f"   Output: {args.output}")
    print()
    
    # 1. Converter dataset
    data_dir = convert_dataset(args.dataset, "./data-mlx")
    
    # 2. Calcular iterations se não especificado
    with open(os.path.join(data_dir, "train.jsonl")) as f:
        num_train = sum(1 for _ in f)
    
    iters = args.iters if args.iters > 0 else num_train * args.epochs
    
    print(f"🚀 Iniciando treino: {iters} iterações ({num_train} exemplos × {args.epochs} épocas)")
    print()
    
    # 3. Criar config YAML para LoRA
    config_path = os.path.join(data_dir, "lora_config.yaml")
    with open(config_path, 'w') as f:
        f.write(f"""# Skynet LoRA config
model: "{args.model}"
data: "{data_dir}"
train: true
fine_tune_type: "lora"
iters: {iters}
batch_size: {args.batch_size}
learning_rate: {args.learning_rate}
num_layers: 16
adapter_path: "{args.output}"
save_every: 50
steps_per_report: 10
steps_per_eval: 50
max_seq_length: 2048
grad_checkpoint: true
""")
    
    # 3. Rodar mlx_lm lora
    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "-c", config_path,
    ]
    
    print(f"📋 Comando: {' '.join(cmd)}")
    print()
    
    # Log pra arquivo + terminal (tee)
    log_file = os.path.join(args.output, "training.log")
    os.makedirs(args.output, exist_ok=True)
    
    print(f"📝 Log: {log_file}")
    print(f"   Acompanhe: tail -f {log_file}")
    print()
    
    with open(log_file, 'w') as lf:
        lf.write(f"=== SKYNET FINE-TUNING ===\n")
        lf.write(f"Modelo: {args.model}\n")
        lf.write(f"Dataset: {args.dataset}\n")
        lf.write(f"Épocas: {args.epochs}\n")
        lf.write(f"Iterações: {iters}\n")
        lf.write(f"Batch: {args.batch_size}\n")
        lf.write(f"LoRA rank: {args.lora_rank}\n")
        lf.write(f"LR: {args.learning_rate}\n\n")
        lf.flush()
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            print(line, end='')
            lf.write(line)
            lf.flush()
        process.wait()
        result_code = process.returncode
    
    if result_code == 0:
        print(f"\n✅ Treino concluído! Adapter salvo em: {args.output}")
        print(f"\n📋 Para testar:")
        print(f'   python3 -m mlx_lm.generate --model {args.model} --adapter-path {args.output} --prompt "Quem é você?"')
        print(f"\n📋 Para fundir modelo completo:")
        print(f"   python3 -m mlx_lm.fuse --model {args.model} --adapter-path {args.output} --save-path ./models/skynet-fused")
    else:
        print(f"\n❌ Erro no treino (exit code: {result_code})")
        sys.exit(1)

if __name__ == "__main__":
    main()
