# 🛡️ TermsBuster – Smart Privacy Policy Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/NLP-Transformers-yellow?logo=huggingface&logoColor=black">
  <img src="https://img.shields.io/badge/ML-Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white">
  <img src="https://img.shields.io/badge/OCR-Tesseract-green">
  <img src="https://img.shields.io/badge/Architecture-Modular-blueviolet">
  <img src="https://img.shields.io/badge/Status-Active-success">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey">
</p>

> AI-powered system that analyzes privacy policies and Terms & Conditions to generate concise summaries, detect high-risk clauses, and assign a structured Privacy Risk Rating — fully offline and privacy-preserving.

---

## 📖 Overview

TermsBuster tackles the growing problem of uninformed digital consent caused by lengthy and legally complex privacy policies.

By combining transformer-based NLP with interpretable risk detection logic, the system improves transparency, compliance awareness, and digital risk assessment.

---

## 📌 Problem Statement

In today’s digital ecosystem, every online platform requires users to accept privacy policies and terms of service. These documents are often:

- Lengthy  
- Filled with legal and technical jargon  
- Difficult for non-technical users to interpret  

As a result, users frequently skip reading them and unknowingly consent to clauses involving data tracking, third-party sharing, and extended data retention.

---

## 💡 Solution

TermsBuster transforms dense legal documents into clear summaries and actionable privacy insights.

It uses:

- A **BART transformer model** for abstractive summarization  
- A **Hybrid AI risk analysis engine** for clause-level detection  
- A structured **Privacy Risk Rating framework (1–5 scale)**  
- Fully offline processing to ensure user confidentiality  

---

## 🚀 Key Features

### 🔹 Multi-Format Document Support
- PDF documents  
- Plain text files  
- Images & screenshots  
- Scanned documents (via OCR)  

### 🔹 AI-Based Summarization
- BART-large-CNN transformer model  
- Context-preserving abstractive summaries  
- Legally coherent output  

### 🔹 Hybrid AI Risk Analyzer

**Combines:**
- TF-IDF keyword weighting  
- Rule-based pattern detection  
- TextRank sentence ranking  
- Safe-phrase filtering  

**Detects risks in:**
- Data collection  
- Third-party sharing  
- Tracking technologies  
- Data retention  
- User consent & rights  

### 🔹 5-Level Privacy Risk Rating
- Very Low → Very High  
- Clause-level tagging  
- Color-coded highlights  
- Interactive Privacy Risk Meter  

### 🔹 Secure Offline Processing
- No cloud uploads  
- No document persistence  
- Fully local execution  

---

## 🏗️ System Architecture
<br>User Input (PDF / Image / Text)
<br>↓
<br>OCR & Text Preprocessing
<br>↓
<br>BART Summarization Engine
<br>↓
<br>Hybrid Risk Analyzer
<br>↓
<br>Privacy Rating Generator
<br>↓
<br>Streamlit Dashboard + Report Export


The modular architecture ensures scalability, maintainability, and future enhancements.

---

## 🛠️ Tech Stack

- Python 3.11+  
- HuggingFace Transformers (BART-large-CNN)  
- PyTorch  
- Scikit-learn (TF-IDF)  
- TextRank  
- Rule-based NLP  
- pytesseract + pdfplumber (OCR)  
- Streamlit  

---

## 📂 Project Structure

termsbuster/
<br>│
<br>├── app.py
<br>├── modules/
<br>│ ├── summarizer.py
<br>│ ├── risk_analyzer.py
<br>│ ├── ocr_reader.py
<br>│ ├── privacy_rating.py
<br>│ └── report_generator.py
<br>├── requirements.txt

---

## 📊 Performance Evaluation

- Accurate OCR extraction across multiple formats  
- High-quality abstractive summarization  
- Reliable clause-level risk detection  
- Consistent 1–5 risk scoring  
- Efficient processing for 5000+ word policies  

The system balances computational efficiency with strong analytical performance.

---

## 🧪 Testing & Validation

- Functional Testing  
- Integration Testing  
- Performance Testing  
- Accuracy Testing  
- Usability Testing  
- Security Testing  

Validated scenarios include:

- Large PDF handling  
- Corrupted file detection  
- Clause identification accuracy  
- Privacy rating consistency  
- Report generation validation  

---

## 🔒 Privacy by Design

- Offline processing  
- No cloud inference  
- No document storage  
- Secure temporary memory handling  

Designed with privacy-first principles to ensure user trust and regulatory alignment.

---

## 🔮 Future Enhancements

- Multi-language policy analysis  
- Real-time policy change monitoring  
- Browser extension integration  
- Compliance auto-mapping  
- Blockchain-based audit trail  
- AI explainer mode for non-technical users  

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/VETRI11K/TermsBuster---Smart-Privacy-Policy-Assistant.git
cd TermsBuster---Smart-Privacy-Policy-Assistant
pip install -r requirements.txt
streamlit run app.py
```

##  Author 
<p><strong>Vetriselvi K</strong></p> <p>MCA – Anna University</p> <p> Data Analyst | Data Specialist</p> 
<p> <a href="https://github.com/VETRI11K"> <img src="https://img.shields.io/badge/GitHub-Profile-black?logo=github"> </a> 
<a href="https://linkedin.com/in/vetriselvi-k-06026b278"> <img src="https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin"> </a> 
</p>

