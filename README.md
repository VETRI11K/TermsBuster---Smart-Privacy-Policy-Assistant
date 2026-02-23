<h1>🛡️TermsBuster---Smart-Privacy-Policy-Assistant</h1><br>
<p><h2>📖 Overview</h2>

TermsBuster is an AI-driven system that analyzes privacy policies and Terms & Conditions to generate concise summaries, detect high-risk clauses, and assign a structured Privacy Risk Rating.

The project addresses the growing issue of uninformed user consent caused by lengthy and legally complex digital policies. By combining transformer models with interpretable risk detection logic, TermsBuster improves transparency, compliance awareness, and digital risk assessment.</p>
<br><br>
<h2>📌 Problem Statement</h2>
<p>
In today’s digital world, every online service and mobile application requires users to accept privacy policies and terms of service. However, these documents are usually lengthy, filled with legal and technical jargon, and difficult for common users to understand. As a result, most people skip reading them and unknowingly consent to clauses that may involve data tracking, third-party sharing, or other privacy risks.
</p>

<h2>💡 Solution</h2>
<p>
TermsBuster bridges this gap by transforming dense legal documents into clear summaries and actionable privacy insights. It uses a transformer-based NLP model to generate concise summaries and a hybrid risk analysis engine to detect high-risk clauses related to data collection, sharing, tracking, and retention. The system assigns a structured privacy risk rating, highlights critical sections, and ensures fully offline processing to maintain user confidentiality and transparency.
</p>

<h2>Key Features</h2>

<h3>🔹 Multi-Format Document Support</h3>
<ul>
  <li>PDF documents</li>
  <li>Plain text files</li>
  <li>Images & screenshots</li>
  <li>Scanned documents (via OCR)</li>
</ul>

<h3>🔹 AI-Based Summarization</h3>
<ul>
  <li>BART transformer model</li>
  <li>Generates concise, legally coherent summaries</li>
  <li>Preserves contextual meaning</li>
</ul>

<h3>🔹 Hybrid AI Risk Analyzer</h3>
<p><strong>Combines:</strong></p>
<ul>
  <li>TF-IDF keyword weighting</li>
  <li>Rule-based pattern detection</li>
  <li>TextRank sentence ranking</li>
  <li>Safe-phrase filtering</li>
</ul>

<p><strong>Detects risks in:</strong></p>
<ul>
  <li>Data collection</li>
  <li>Third-party sharing</li>
  <li>Tracking technologies</li>
  <li>Data retention</li>
  <li>User consent & rights</li>
</ul>

<h3>🔹 5-Level Privacy Risk Rating</h3>
<ul>
  <li>Very Low → Very High</li>
  <li>Clause-level risk tagging</li>
  <li>Color-coded highlights</li>
  <li>Interactive Privacy Risk Meter</li>
</ul>

<h3>🔹 Secure Offline Processing</h3>
<ul>
  <li>No cloud uploads</li>
  <li>No document storage</li>
  <li>Fully local execution</li>
</ul>

<h2>System Architecture</h2>
<p>
User Input (PDF / Image / Text)<br>
↓<br>
OCR & Text Preprocessing<br>
↓<br>
BART Summarization Engine<br>
↓<br>
Hybrid Risk Analyzer<br>
↓<br>
Privacy Rating Generator<br>
↓<br>
Streamlit Dashboard + Report Export
</p>
<p>
The modular architecture ensures scalability and easy enhancement.
</p>

<hr>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li><strong>Python 3.11+</strong></li>
  <li><strong>HuggingFace Transformers (BART-large-CNN)</strong></li>
  <li><strong>PyTorch</strong></li>
  <li><strong>Scikit-learn (TF-IDF)</strong></li>
  <li><strong>TextRank</strong></li>
  <li><strong>Rule-based NLP</strong></li>
  <li><strong>pytesseract + pdfplumber (OCR)</strong></li>
  <li><strong>Streamlit (UI)</strong></li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
termsbuster/
│
├── app.py
├── modules/
│   ├── summarizer.py
│   ├── risk_analyzer.py
│   ├── ocr_reader.py
│   ├── privacy_rating.py
│   └── report_generator.py
│
├── requirements.txt
└── README.md
</pre>

<hr>

<h2>📊 Performance Evaluation</h2>
<ul>
  <li>Accurate OCR extraction across multiple formats</li>
  <li>High-quality abstractive summarization</li>
  <li>Reliable clause-level risk detection</li>
  <li>Consistent 1–5 risk scoring</li>
  <li>Efficient processing for 5000+ word policies</li>
</ul>

<p>
The system balances performance efficiency with strong analytical accuracy.
</p>

<hr>

<h2> Testing & Validation</h2>
<ul>
  <li>Functional Testing</li>
  <li>Integration Testing</li>
  <li>Performance Testing</li>
  <li>Accuracy Testing</li>
  <li>Usability Testing</li>
  <li>Security Testing</li>
</ul>

<ul>
  <li>Large PDF handling</li>
  <li>Corrupted file handling</li>
  <li>Clause detection accuracy</li>
  <li>Privacy rating consistency</li>
  <li>Report generation validation</li>
</ul>

<hr>

<h2>🔒 Privacy by Design</h2>
<ul>
  <li>Offline processing</li>
  <li>No cloud inference</li>
  <li>No document persistence</li>
  <li>Secure temporary memory handling</li>
</ul>

<hr>

<h2>🔮 Future Enhancements</h2>
<ul>
  <li>Multi-language policy analysis</li>
  <li>Real-time policy change monitoring</li>
  <li>Browser extension integration</li>
  <li>Compliance auto-mapping</li>
  <li>Blockchain-based audit trail</li>
  <li>AI explainer mode for non-technical users</li>
</ul>

<hr>

<h2>👩‍💻 Author</h2>

<p><strong>Vetriselvi K</strong></p>
<p>MCA – Anna University</p>
<p>AI Engineer | NLP & Privacy Risk Analytics Specialist</p>

<p>
<a href="https://github.com/VETRI11K">
<img src="https://img.shields.io/badge/GitHub-Profile-black?logo=github">
</a>

<a href="https://linkedin.com/in/vetriselvi-k-06026b278">
<img src="https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin">
</a>
</p>
