import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
import torch
import textwrap

# ----------------------------------------
# Load DistilBART model (optimized for CPU) with caching
# ----------------------------------------
MODEL_PATH = "sshleifer/distilbart-cnn-12-6"

@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BartTokenizer.from_pretrained(MODEL_PATH)
    model = BartForConditionalGeneration.from_pretrained(MODEL_PATH).to(device)
    print(f"✅ Model loaded on: {device}")
    return tokenizer, model, device

# ----------------------------------------
# Summarization with caching
# ----------------------------------------
@st.cache_data
def summarize_text(text, max_length=250, min_length=80):
    """Generate a concise, readable summary using DistilBART (optimized for CPU)."""
    if not text or len(text.strip()) == 0:
        return "No valid text provided for summarization."

    tokenizer, model, device = load_model()
    with torch.no_grad():  # disable gradient tracking for speed
        inputs = tokenizer([text], max_length=1024, truncation=True, return_tensors="pt").to(device)
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=2,               # reduced from 4 to 2 for faster run
            length_penalty=1.5,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True,
            no_repeat_ngram_size=3     # avoid repetitive output
        )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return "\n".join(textwrap.wrap(summary, width=100))

# ----------------------------------------
# Chunk Summarization (for long documents)
# ----------------------------------------
def chunk_and_summarize(text):
    """Split long text into manageable chunks and summarize each."""
    chunk_size = 900
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = [summarize_text(chunk) for chunk in chunks]
    return "\n".join(summaries)

# ----------------------------------------
# AI Smart Confidence Metric
# ----------------------------------------
def calculate_summary_confidence(text, summary):
    """
    Estimate AI summary confidence based on keyword coverage and summary length ratio.
    """
    if not text or not summary:
        return 0

    key_terms = [
        "data", "privacy", "personal", "information",
        "collect", "use", "share", "store", "retain",
        "third", "party"
    ]
    matched = sum(1 for term in key_terms if term in summary.lower())
    coverage = matched / len(key_terms)

    ratio = len(summary) / max(len(text), 1)
    ratio_score = 1 - abs(ratio - 0.1)  # ideal ratio ~10%
    ratio_score = max(0, ratio_score)

    confidence = int((0.6 * coverage + 0.4 * ratio_score) * 100)
    return min(confidence, 99)
