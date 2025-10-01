from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ---------------------------
# Load model once at startup
# ---------------------------
MODEL_DIR = "D:\\FYP\\CloneRepo\\FYP\\middleware_flan_3t5_base" 

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# ---------------------------
# FastAPI app setup
# ---------------------------
app = FastAPI(title="Prompt Generation Middleware API")

class RequestData(BaseModel):
    language: str
    topics: List[str]
    difficulty: str
    max_input_length: int = 128
    max_output_length: int = 128
    num_return_sequences: int = 1


@app.post("/generate")
def generate(data: RequestData):
    # Prepare input text
    topics_str = ", ".join(data.topics)
    input_text = f"language: {data.language} | topics: {topics_str} | difficulty: {data.difficulty}"

    # Tokenize
    inputs = tokenizer(
        [input_text],
        max_length=data.max_input_length,
        truncation=True,
        return_tensors="pt"
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Generate
    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=data.max_output_length,
        num_beams=4,
        early_stopping=True,
        num_return_sequences=data.num_return_sequences,
        no_repeat_ngram_size=2,
        length_penalty=1.0,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    decoded = [tokenizer.decode(g, skip_special_tokens=True).strip() for g in outputs]

    return {"prompt": decoded}
