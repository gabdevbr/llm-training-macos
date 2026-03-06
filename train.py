#!/usr/bin/env python3
"""
Fine-tuning Skynet — Script de treinamento com unsloth + LoRA

Este script treina um modelo Llama 3.1 com contexto do Gab.
Usa LoRA (Low-Rank Adaptation) pra ser rápido e eficiente em memória.

Modo de uso:
    python3 train.py --model_name unsloth/llama-3.1-8b-bnb-4bit --dataset_path dataset.jsonl
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict

# === IMPORTS: unsloth + transformers ===
from unsloth import FastLanguageModel, get_chat_template
from transformers import (
    TrainingArguments,
    TextIterableDataset,
    DataCollatorForSeq2Seq,
)
from trl import SFTTrainer
import torch
from datasets import load_dataset, Dataset


# === FUNÇÃO 1: Carregar dataset JSONL ===
def load_jsonl_dataset(path: str) -> List[Dict]:
    """
    Lê arquivo JSONL (seu contexto) e formata para treinamento.
    
    Arquivo esperado:
        {"instruction": "...", "response": "..."}
        {"instruction": "...", "response": "..."}
    
    Retorna:
        Lista de dicts com 'text' formatado para o modelo.
    """
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                example = json.loads(line)
                # Formata: [INST] instruction [/INST] response
                text = f"[INST] {example['instruction']} [/INST] {example['response']}"
                data.append({"text": text})
    
    print(f"✅ Carregou {len(data)} exemplos do dataset")
    return data


# === FUNÇÃO 2: Configurar modelo ===
def setup_model(model_name: str, max_seq_length: int = 2048):
    """
    Carrega modelo Llama 3.1 + aplica LoRA adapters.
    
    Parâmetros:
        model_name: ID do modelo (ex: unsloth/llama-3.1-8b-bnb-4bit)
        max_seq_length: Máximo tokens por exemplo
    
    Retorna:
        (model, tokenizer) configurados com LoRA
    """
    
    # Carrega modelo em 4-bit quantization (reduz memória)
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=torch.float16,  # Precisão reduzida (ok pro Mac)
        load_in_4bit=True,    # Quantização 4-bit
    )
    
    # Aplica LoRA (adapters treináveis)
    # Só ~2% dos pesos são treináveis, resto congelado
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,                  # Rank (tamanho do adapter)
        lora_alpha=16,        # Scaling
        lora_dropout=0.05,    # Regularização
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )
    
    print(f"✅ Modelo configurado: {model_name}")
    print(f"   LoRA rank: 16, dropout: 0.05")
    return model, tokenizer


# === FUNÇÃO 3: Treinar ===
def train(
    model,
    tokenizer,
    dataset_path: str,
    output_dir: str = "./models/skynet-v1",
    num_epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 0.0002,
    max_seq_length: int = 2048,
):
    """
    Fine-tuna o modelo com seu contexto (JSONL).
    
    Parâmetros:
        model: modelo FastLanguageModel
        tokenizer: tokenizer associado
        dataset_path: caminho pro dataset.jsonl
        output_dir: onde salvar checkpoints
        num_epochs: quantas voltas nos dados
        batch_size: exemplos por iteração
        learning_rate: taxa de aprendizado
        max_seq_length: máximo tokens por exemplo
    """
    
    # Carrega dataset
    data = load_jsonl_dataset(dataset_path)
    dataset = Dataset.from_dict({"text": [d["text"] for d in data]})
    
    # Configuração de treinamento
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=1,
        learning_rate=learning_rate,
        lr_scheduler_type="linear",
        logging_steps=10,
        save_steps=50,
        save_total_limit=3,
        optim="paged_adamw_8bit",  # Otimizador eficiente
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        weight_decay=0.01,
        # Desabilita wandb (logging local)
        report_to="none",
        # Salva modelo ao final
        save_strategy="epoch",
    )
    
    # Trainer (gerencia o loop de treinamento)
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        args=training_args,
        max_seq_length=max_seq_length,
    )
    
    print(f"🚀 Iniciando treino...")
    print(f"   Epochs: {num_epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   Salva em: {output_dir}")
    
    # Roda o treino
    trainer.train()
    
    print(f"✅ Treino concluído!")
    print(f"   Modelo salvo em: {output_dir}")
    
    return model, trainer


# === FUNÇÃO 4: Exportar para Ollama ===
def export_to_ollama(model, tokenizer, output_dir: str = "./models/skynet-v1"):
    """
    Converte modelo fine-tuned para formato Ollama (GGUF).
    
    Isso torna o modelo rodável com `ollama run skynet`.
    """
    
    # Mescla LoRA com modelo base
    model = model.merge_and_unload()
    
    # Salva em formato HF (Hugging Face)
    model.save_pretrained(f"{output_dir}/hf-model")
    tokenizer.save_pretrained(f"{output_dir}/hf-model")
    
    print(f"✅ Modelo exportado para {output_dir}/hf-model")
    print(f"\n📝 Próximo passo: converter pra GGUF com llama.cpp")
    print(f"   (unsloth faz isso automaticamente, veja docs)")


# === MAIN ===
def main():
    parser = argparse.ArgumentParser(description="Fine-tune Skynet")
    parser.add_argument("--model_name", default="unsloth/llama-3.1-8b-bnb-4bit")
    parser.add_argument("--dataset_path", default="dataset.jsonl")
    parser.add_argument("--output_dir", default="./models/skynet-v1")
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=0.0002)
    parser.add_argument("--max_seq_length", type=int, default=2048)
    
    args = parser.parse_args()
    
    # Verifica se dataset existe
    if not Path(args.dataset_path).exists():
        print(f"❌ Dataset não encontrado: {args.dataset_path}")
        return
    
    # Configura modelo
    model, tokenizer = setup_model(args.model_name, args.max_seq_length)
    
    # Treina
    model, trainer = train(
        model,
        tokenizer,
        dataset_path=args.dataset_path,
        output_dir=args.output_dir,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        max_seq_length=args.max_seq_length,
    )
    
    # Exporta
    export_to_ollama(model, tokenizer, args.output_dir)
    
    print("\n" + "="*60)
    print("🎉 Fine-tuning concluído!")
    print("="*60)


if __name__ == "__main__":
    main()
