import json
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model


def fine_tune(data_file="data/ready_to_train.json", model_name="meta-llama/Llama-3-7b"):
    with open(data_file) as f:
        samples = json.load(f)

    texts = [
        f"Input: {s['predictions']} | Reference: {s['references']} | Stats: {s['stats']}"
        for s in samples
    ]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    encodings = tokenizer(texts, truncation=True, padding=True, return_tensors="pt")

    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.1,
        bias="none"
    )
    model = get_peft_model(model, lora_config)

    args = TrainingArguments(
        output_dir="./fine_tuned",
        per_device_train_batch_size=2,
        num_train_epochs=3,
        learning_rate=3e-4,
        logging_steps=10
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=encodings["input_ids"]
    )
    trainer.train()
    print("[🚀] Fine-tuning complete")
