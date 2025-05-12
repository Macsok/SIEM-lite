from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Inicjalizacja modelu
_tokenizer = None


def init_llm():
    global _model, _tokenizer
    if _model is None:
        model_name = "distilgpt2"  # Lżejsza wersja GPT-2
        _tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        _model = GPT2LMHeadModel.from_pretrained(model_name, torch_dtype=torch.float16)
        _tokenizer.pad_token = _tokenizer.eos_token


def analyze_log_with_llm(log_text: str, max_tokens: int = 100) -> str:
    init_llm()

    prompt = f"""
    [Analiza SOC] Oceń następujący log:
    1. Poziom zagrożenia: (niskie/średnie/wysokie)
    2. Opis zdarzenia: 
    3. Zalecane działania:

    Log: {log_text}
    """

    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = _model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=max_tokens,
        pad_token_id=_tokenizer.eos_token_id
    )

    return _tokenizer.decode(outputs[0], skip_special_tokens=True)