from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

_tokenizer = None
_model = None


def init_llm():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        model_name = "google/flan-t5-small"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def analyze_log_with_llm(log_text: str, max_tokens: int = 200) -> str:
    init_llm()

#mprompt dla modelu
    prompt = f"""
    The following system logs have been detected:

    {log_text}

    Please provide a list of recommendations for the SOC administrator:

    - What do these events mean?
    - What are the potential threats?
    - What actions should be taken?
        """

    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = _model.generate(**inputs, max_new_tokens=max_tokens)

    return _tokenizer.decode(outputs[0], skip_special_tokens=True)
