import json
import re
import streamlit as st
from typing import Dict, List, Tuple
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from collections import Counter

# ------------------------------
# Negation Words
# ------------------------------
NEGATION_WORDS = [
    r"\bno\b", r"\bnot\b", r"\bnever\b", r"\bdon't\b", r"\bdoesn't\b", r"\bdoes not\b",
    r"\bdidn't\b", r"\bdid not\b", r"\bwithout\b", r"\bno longer\b", r"\bcannot\b", r"\bcan't\b",
    r"\bexclude\b", r"\bexcept\b"
]
NEGATION_RE = re.compile("|".join(NEGATION_WORDS), flags=re.IGNORECASE)

# ------------------------------
# Safe phrases (loaded once)
# ------------------------------
SAFE_PHRASES_PATH = Path("data/safe_phrases.json")
if SAFE_PHRASES_PATH.exists():
    try:
        with SAFE_PHRASES_PATH.open("r", encoding="utf-8") as f:
            _safe_obj = json.load(f)
        SAFE_PHRASES = {p.lower() for p in _safe_obj.get("safe_phrases", [])}
    except Exception:
        SAFE_PHRASES = set()
else:
    SAFE_PHRASES = set()

def is_safe_sentence(sentence: str) -> bool:
    """Skip scoring if sentence contains protective safe phrases."""
    if not SAFE_PHRASES:
        return False
    s = (sentence or "").lower()
    for phrase in SAFE_PHRASES:
        if phrase and phrase in s:
            return True
    return False

# ------------------------------
# TF-IDF Risk Density
# ------------------------------
def get_tfidf_density(text: str, risk_data: Dict) -> float:
    """% of policy vocabulary containing risky terms (density score)."""
    try:
        # Extract top risky keywords
        risk_keywords = []
        for level_items in risk_data.values():
            for item in level_items[:20]:  # top 20 per level
                kw = item.get("keyword", "").lower().strip()
                if kw and len(kw.split()) <= 3:
                    risk_keywords.append(kw)
        
        sentences = re.split(r'(?<=[\.?!])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) < 2:
            return 0.0
        
        vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1,2))
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        
        risk_hits = sum(1 for kw in set(risk_keywords) if kw in feature_names)
        total_terms = len(feature_names)
        
        density = (risk_hits / total_terms * 100) if total_terms > 0 else 0
        return min(100, density)
    except:
        return 0.0

# ------------------------------
# TextRank Top Risk Phrases
# ------------------------------
def extract_textrank_phrases(text: str, max_phrases: int = 5) -> List[str]:
    """Extract top risky phrases using TextRank graph algorithm."""
    try:
        sentences = re.split(r'(?<=[\.?!])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) < 3:
            return []
        
        # Build sentence similarity graph
        graph = nx.Graph()
        for i, s1 in enumerate(sentences):
            for j, s2 in enumerate(sentences[i+1:], i+1):
                # Simple overlap similarity
                words1 = set(re.findall(r'\w+', s1.lower()))
                words2 = set(re.findall(r'\w+', s2.lower()))
                overlap = len(words1 & words2)
                if overlap > 1:
                    graph.add_edge(i, j, weight=overlap)
        
        if len(graph.nodes) == 0:
            return sentences[:max_phrases]
        
        # TextRank scores
        scores = nx.pagerank(graph, alpha=0.85)
        top_indices = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_phrases]
        
        return [sentences[i] for i, _ in top_indices]
    except:
        sentences = re.split(r'(?<=[\.?!])\s+', text)
        return [s.strip() for s in sentences[:5] if s.strip()]

# ------------------------------
# Load JSON with caching
# ------------------------------
@st.cache_data(show_spinner=False)
def cached_load_risk_data(json_path: str) -> Dict:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------------
# Clean Text
# ------------------------------
def clean_text(text: str) -> str:
    if text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ------------------------------
# Extract Sentence
# ------------------------------
def sentence_for_index(text: str, start: int, end: int) -> str:
    sentences = re.split(r'(?<=[\.?!])\s+', text)
    pos = 0
    for s in sentences:
        next_pos = pos + len(s)
        if start >= pos and start <= next_pos:
            return s.strip()
        pos = next_pos + 1
    return text[max(0, start - 80): end + 80].strip()

# ------------------------------
# Negation Check
# ------------------------------
def has_negation_around(text: str, match_start: int, window_chars: int = 50) -> bool:
    window_start = max(0, match_start - window_chars)
    context = text[window_start:match_start]
    return bool(NEGATION_RE.search(context))

# ------------------------------
# Keyword Match
# ------------------------------
def detect_matches(combined_text: str, keyword: str) -> List[Tuple[int, int, str]]:
    pattern = r"\b" + re.escape(keyword) + r"\b"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    matches = []
    for m in regex.finditer(combined_text):
        start, end = m.start(), m.end()
        sent = sentence_for_index(combined_text, start, end)
        matches.append((start, end, sent))
    return matches

# ------------------------------
# Severity Mapping
# ------------------------------
def map_level_severity(level_key: str) -> str:
    k = level_key.lower()
    if "very_high" in k or "critical" in k:
        return "very_high_risk"
    if "high" in k:
        return "high_risk"
    if "moderate" in k or "medium" in k:
        return "moderate_risk"
    if "low" in k:
        return "low_risk"
    if "minimal" in k:
        return "minimal_risk"
    return "moderate_risk"

# ------------------------------
# Cache Analyze Policy result
# ------------------------------
@st.cache_data(show_spinner=True)
def cached_analyze_policy(extracted_text: str, summarized_text: str, json_path: str) -> Dict:
    risk_data = cached_load_risk_data(json_path)
    combined_text = clean_text(f"{extracted_text or ''} {summarized_text or ''}")

    total_score = 0
    severity_counters = {
        "very_high_risk": 0, "high_risk": 0, "moderate_risk": 0,
        "low_risk": 0, "minimal_risk": 0
    }
    matched: Dict[str, Dict] = {}

    # 1. Keyword matching with safe phrase filtering
    for level_key, items in risk_data.items():
        matched.setdefault(level_key, {})
        for item in items:
            keyword = clean_text(item.get("keyword", ""))
            if not keyword:
                continue

            score = int(item.get("score", 0))
            occurrences = detect_matches(combined_text, keyword)

            valid_count = 0
            sentences: List[str] = []
            for (start, end, sentence) in occurrences:
                # Skip safe sentences
                if is_safe_sentence(sentence):
                    continue
                # Skip negated matches
                if has_negation_around(combined_text, start):
                    continue
                
                valid_count += 1
                sentences.append(sentence)

            if valid_count > 0:
                effective_count = min(valid_count, 3)
                matched[level_key][keyword] = {
                    "count": valid_count,
                    "score_each": score,
                    "total_score": score * effective_count,
                    "sentences": sentences
                }
                total_score += score * effective_count
                sev = map_level_severity(level_key)
                severity_counters[sev] += 1

    # 2. TF-IDF Risk Density
    tfidf_density = get_tfidf_density(combined_text, risk_data)

    # 3. TextRank Top Risk Phrases
    top_risk_phrases = extract_textrank_phrases(combined_text)

    # Risk Level determination
    if severity_counters["very_high_risk"] > 0 and total_score >= 200:
        final_level = "Very High Risk"
    elif total_score >= 160:
        final_level = "High Risk"
    elif total_score >= 100:
        final_level = "Moderate Risk"
    elif total_score >= 50:
        final_level = "Low Risk"
    elif 0 < total_score <= 20:
        final_level = "Minimal Risk"
    else:
        final_level = "No Risk Detected"

    confidence = min(95, 50 + int(total_score * 0.2 + tfidf_density * 0.3))

    return {
        "Total Score": total_score,
        "Risk Level": final_level,
        "Confidence": confidence,
        "TF-IDF Density": round(tfidf_density, 1),
        "Top Risk Phrases": top_risk_phrases,
        "Matches": matched,
    }
