
import streamlit as st
from PIL import Image
import pdfplumber
import pytesseract  
import time
import pandas as pd

from modules.exporter import generate_pdf_report, generate_image_report
from modules.summarizer import summarize_text
from modules.risk_analyzer import cached_analyze_policy
from modules.ai_explainer import generate_ai_friendly_explanation

if "show_matches" not in st.session_state:
    st.session_state["show_matches"] = False

st.markdown("""
    <style>
        /* Hide default Streamlit header */
        header[data-testid="stHeader"] {visibility: hidden; height: 0;}
        
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="TermsBuster", page_icon=":guardsman:", layout="centered")

# --- Hide default Streamlit UI ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] {visibility: hidden; height: 0;}
        .reportview-container {margin-top: -2em;}
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- Custom CSS ---
st.markdown("""
    <style>
    body {background-color:#020617;}
    .navbar {
        width: 100vw;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #111827;
        border-radius: 0;
        padding: 14px 32px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px #0007;
        z-index: 9999;
    }
    .main-title, .search-container, .subtitle, .tagline {
        margin-top: 80px;
    }
    .nav-link {
        color: #e5e7eb !important;
        text-decoration: none !important;
        font-size: 1.0em;
        margin: 0 16px;
        transition: color 0.2s;
        cursor: pointer;
    }
    .nav-link:hover {
        color: #ffe56b !important;
    }
    .nav-spacer {flex: 1;}
    .refresh-btn {
        background: #10b981;
        color: #fff;
        border-radius: 18px;
        border: none;
        padding: 4px 18px;
        font-size: 0.95em;
        cursor: pointer;
        margin-left: 10px;
    }
    .main-title { 
        font-size: 3em; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 30px; 
        color:#f9fafb;
    }
    .subtitle { 
        font-size: 1.2em; 
        text-align: center; 
        color: #ffe56b; 
        margin: 12px 0 4px 0; 
    }
    .tagline { 
        font-size: 1.05em; 
        text-align: center; 
        color: #9ca3af; 
        margin-bottom: 22px; 
    }
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 24px 0 20px 0;
    }
    .about-box {
        background: #111827;
        border-radius: 22px;
        padding: 32px 38px;
        margin-top: 26px;
        color: #e5e7eb;
        box-shadow: 0 4px 20px #0003;
        font-size: 1.05em;
    }
    .about-box h1 {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 16px;
    }
    .about-box hr {
        margin: 16px 0;
        border: 1px solid #374151;
    }
    .block-container {padding-top: 80px !important;}
    .risk-banner { 
        background: #ffe56b; 
        color: #272300; 
        padding: 14px 18px; 
        border-radius:10px; 
        font-weight:600; 
        font-size:1.05em; 
        margin:20px 0; 
        text-align:center;
    }
    .summary-card { 
        background: #f9f9f9; 
        color: #111;
        border-left: 4px solid #158cff; 
        border-radius: 8px; 
        padding: 16px 20px; 
        margin:16px 0; 
        font-size: 1.02em; 
    }
    .advice-box { 
        background: #fdf5db; 
        color: #333; 
        border-radius: 12px; 
        padding: 16px 24px; 
        font-size: 1.02em; 
        font-weight: 500; 
        margin:20px 0;
    }
    .score-highlight { 
        background: #e3f2fd; 
        color: #000;
        border-radius: 10px; 
        padding: 18px; 
        margin: 16px 0; 
        text-align: center; 
        font-size: 1.1em; 
        font-weight: bold; 
    }
    footer {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- Navbar using query params (good look) ---
def navbar(active_page="Home"):
    st.markdown(f"""
        <div class="navbar">
            <form action="" method="get" style="display:inline;">
                <input type="hidden" name="page" value="Home">
                <button class="nav-link" type="submit"
                    style="background:none;border:none;padding:0;cursor:pointer;color:{'#ffe56b' if active_page=='Home' else '#e5e7eb'};">
                    Home
                </button>
            </form>
            <form action="" method="get" style="display:inline;">
                <input type="hidden" name="page" value="About">
                <button class="nav-link" type="submit"
                    style="background:none;border:none;padding:0;cursor:pointer;color:{'#ffe56b' if active_page=='About' else '#e5e7eb'};">
                    About
                </button>
            </form>
            <form action="" method="get" style="display:inline;">
                <input type="hidden" name="page" value="Download">
                <button class="nav-link" type="submit"
                    style="background:none;border:none;padding:0;cursor:pointer;color:{'#ffe56b' if active_page=='Download' else '#e5e7eb'};">
                    Download
                </button>
            </form>
            <div class="nav-spacer"></div>
            <form action="" method="get" style="display:inline;">
                <button class="refresh-btn" type="submit" name="action" value="refresh">
                    Refresh
                </button>
            </form>
        </div>
    """, unsafe_allow_html=True)

# --- Text Extraction ---
def extract_text(file):
    if not file:
        return ""
    file.seek(0)
    if file.type == "application/pdf":
        try:
            with pdfplumber.open(file) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
            return "\n".join(pages)
        except:
            return "PDF extraction failed."
    if file.type.startswith("image/"):
        try:
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
        except:
            return "Image extraction failed."
        return text if text.strip() else "No text detected in the image."
    if file.type == "text/plain":
        try:
            return file.read().decode("utf-8")
        except:
            return "TXT extraction failed."
    return ""

# --- Dynamic Advice ---
def dynamic_user_advice(risklevel, totalscore):
    lev = risklevel.lower()
    if "high" in lev or totalscore >= 160:
        return "⚠️ Heads up: This policy may put your privacy at risk. Limit what you share and double-check the settings!"
    elif "moderate" in lev or totalscore >= 120:
        return "This policy has some risks. Review what you're approving—especially sharing, profiling, and tracking options."
    elif "low" in lev or totalscore >= 50:
        return "Good news: Most risks are low. Still, check privacy options and keep an eye on future updates."
    else:
        return "No major risk detected. You can proceed, but it's wise to stay informed about any changes."

# --- Home Page ---
def home_page():
    st.markdown('<div class="main-title">TermsBuster - Smart Privacy Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered Privacy Policy Analyzer</div>', unsafe_allow_html=True)
    st.markdown("""
        <p class="tagline">
        Cuts through the fine print and gives you the truth companies don&apos;t want you to see.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('<div class="search-container"></div>', unsafe_allow_html=True)

    text_query = st.text_area("📎 Paste policy text here", height=140, placeholder="Paste privacy policy text...")
    uploaded = st.file_uploader("📁 Upload Privacy Policy (PDF/Image/Text)", type=["pdf", "png", "jpg", "jpeg", "txt"], key="file_upload_1")

    text = ""
    extraction_shown = False
    if uploaded:
        text = extract_text(uploaded)
        extraction_shown = True
        if text:
            st.subheader("✏️ Extracted Text")
            st.text_area("Extracted Content", text, height=200, disabled=True)
        else:
            st.error("No text found! If this is a scanned PDF, OCR is not applied automatically. Try converting PDF pages to images and upload as PNG/JPEG.")
    elif text_query.strip():
        text = text_query.strip()

    analyze_clicked = st.button("🔍 Analyze with AI")

    if analyze_clicked and text:
        if not extraction_shown:
            st.subheader("✏️ Extracted Text")
            st.text_area("Extracted Content", text, height=200, disabled=True)

        with st.spinner("AI is analyzing the policy..."):
            start_time = time.time()

            # Summary
            try:
                st.info("AI is analyzing the policy... please wait ⏳")
                summary = summarize_text(text)
            except Exception:
                summary = "⚠️ Could not generate summary. Using placeholder."

            # Explanation
            try:
                explanation_md = generate_ai_friendly_explanation(summary)
            except Exception:
                explanation_md = "- Could not generate explanation. Using placeholder."

            # Risk analysis
            try:
                result = cached_analyze_policy(text, summary, "data/risk_analyzer_MASTER_FINAL.json")
            except Exception:
                result = {"Total Score": 5, "Risk Level": "Moderate Risk", "Confidence": 80, "Matches": {}}

            risklevel = result.get("Risk Level", "Unknown")
            confidence = result.get("Confidence", 50)
            totalscore = result.get("Total Score", 0)
            matches = result.get("Matches", {})

            # Save latest analysis in session_state
            st.session_state["policy_text"] = text
            st.session_state["summary"] = summary
            st.session_state["risk_level"] = risklevel
            st.session_state["confidence"] = confidence
            st.session_state["total_score"] = totalscore
            st.session_state["matches"] = matches

            # --- also persist latest analysis to disk for Download page ---
            import json
            from pathlib import Path

            ANALYSIS_PATH = Path("data/latest_analysis.json")
            latest = {
                "policy_text": text,
                "summary": summary,
                "risk_level": risklevel,
                "confidence": confidence,
                "total_score": totalscore,
                "matches": matches,          # ← ADD THIS
            }
            ANALYSIS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with ANALYSIS_PATH.open("w", encoding="utf-8") as f:
                json.dump(latest, f)


            # Also push key scores into URL (for cross-session fallback)
            st.query_params.update({
                "page": "Home",
                "risk_level": risklevel,
                "confidence": str(confidence),
                "total_score": str(totalscore),
            })

            # --- OUTPUT SECTION ---
            st.markdown("---")
            st.markdown('<div class="risk-banner">⚠️ We found some privacy risks in this policy. Please check the details below.</div>', unsafe_allow_html=True)

            st.subheader("📋 What's This Policy Really About?")
            st.markdown(f'<div class="summary-card">{summary}</div>', unsafe_allow_html=True)

            st.subheader("✨ Policy In Simple Terms")
            st.markdown(explanation_md)

            st.subheader("🛡️ How Safe Is Your Data?")
            risk_rows = []
            for key_level, label in [
                ("very_high_risk", "Very High"),
                ("high_risk", "High"),
                ("moderate_risk", "Moderate"),
                ("low_risk", "Low")
            ]:
                level_data = matches.get(key_level, {})
                for kw, detail in level_data.items():
                    risk_rows.append(
                        {"Risk Level": label, "Keyword": kw, "Score": detail.get("score_each", 0)}
                    )

            # if risk_rows:
            #     df = pd.DataFrame(risk_rows)
            #     st.dataframe(df, use_container_width=True, hide_index=True)
            # else:
            #     st.write("No significant risk keywords detected.")

            st.markdown(
                f'<div class="score-highlight">'
                f'🎯 <b>Privacy Rating:</b> {risklevel}<br>'
                f'📊 <b>Total Risk Score:</b> {totalscore} &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'🔒 <b>Confidence:</b> {confidence}/100'
                f'</div>',
                unsafe_allow_html=True
            )
        # NEW: show TF-IDF Density and Top Phrases count (if present)
            tfidf_density = result.get("TF-IDF Density", 0)
            topphrases = result.get("Top Risk Phrases", [])

            st.markdown(
                f'<div class="score-highlight">'
                f'📈 <b>TF-IDF Risk Density:</b> {tfidf_density}%<br>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Show Top Risk Phrases only for High / Very High
            if risklevel in ["Very High Risk", "High Risk"] and topphrases:
                st.subheader("Top Risk Phrases (NLP)")
                for i, phrase in enumerate(topphrases[:5], 1):
                    st.markdown(f"{i}. {phrase}")


            st.subheader("🎯 How Sure Are We?")
            st.progress(confidence / 100)
            st.write(f"**Confidence Level:** {confidence}%")

            st.markdown(
                f'<div class="advice-box">'
                f'💡 <b>Our Advice For You:</b><br>{dynamic_user_advice(risklevel, totalscore)}'
                f'</div>',
                unsafe_allow_html=True
            )

            elapsed = round(time.time() - start_time, 2)
            st.success(f"✅ Analysis completed in {elapsed} seconds.")

            # Matching keywords & sentences (dropdown only)
            st.subheader("📄 Matching Keywords & Sentences")
            with st.expander("Click to view matched keywords and real policy sentences", expanded=False):
                found = False
                for level_key, level_data in matches.items():
                    if not level_data:
                        continue
                    for kw, detail in level_data.items():
                        sentences_list = detail.get("sentences", [])
                        if sentences_list:
                            st.markdown(f"**{kw}** *(Risk: {level_key.replace('_', ' ').title()})*")
                            for sent in sentences_list:
                                st.markdown(f"- {sent.strip()}")
                            found = True
                if not found:
                    st.info("No keyword matches with sentences were found in this policy.")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown('<small style="display:block; text-align:center; color:#6b7280;">Made with ❤️ by TermsBuster • Powered by AI</small>', unsafe_allow_html=True)

# --- About Page ---
def about_page():
    st.header("About Us - 🛡️TermsBuster")
    st.markdown("""
At TermsBuster, we believe that understanding privacy should never feel complicated. Today, almost every app or website comes with long privacy policies that customers rarely read — not because they don’t care, but because these documents are filled with legal language and difficult-to-follow terms.

**TermsBuster was created to solve this problem.**
We make privacy information clear, simple, and easy to understand so users can confidently decide how their data is being used.

---

### Our Mission
Our mission is straightforward:  
To help people understand what they’re agreeing to before sharing their personal information online. We aim to bring clarity, transparency, and trust into digital interactions.

---

### What We Do

- **Easy-to-Read Summaries**  
  We convert long privacy policies into short, friendly summaries that anyone can understand, without losing important details.

- **Risk Highlights**  
  Our system scans each policy to identify potential risks, such as data sharing, tracking, or unclear consent. We highlight these points clearly so users know what to watch out for.

- **Privacy Rating**  
  Every policy gets a simple Privacy Rating, helping users quickly see how trustworthy a service is when it comes to data handling.

- **Document & Screenshot Support**  
  Users can upload files or screenshots, and our OCR engine reads and analyzes them instantly.


---

### Why TermsBuster Matters
Most people agree to terms without reading them — not because they don’t want to, but because the policies are written in a way that’s hard to follow. This gap creates risks.
TermsBuster makes privacy understandable for everyone, regardless of age, background, or technical knowledge.

---

### Our Vision
We want to build a world where digital privacy is transparent, user-friendly, and accessible to all.
TermsBuster aims to become a trusted companion for anyone who wants to stay informed and safe online.
""")


# --- Download Page ---
def download_page():
    st.markdown("""
        <div class="about-box" style="text-align:center; padding-bottom:32px;">
            <h1>Download TermsBuster Results</h1>
            <hr>
            <p>Export your analysis as PDF or image for sharing or reporting.</p>
        </div>
    """, unsafe_allow_html=True)

    qp = st.query_params

    import json
    from pathlib import Path

    qp = st.query_params
    ANALYSIS_PATH = Path("data/latest_analysis.json")

    # 1) try session_state first
    policy_text = st.session_state.get("policy_text", "")
    summary = st.session_state.get("summary", "")
    matches = st.session_state.get("matches", {})
    risk_level = st.session_state.get("risk_level", qp.get("risk_level", "Unknown"))
    try:
        confidence = st.session_state.get("confidence", int(qp.get("confidence", 0)))
    except ValueError:
        confidence = 0
    try:
        total_score = st.session_state.get("total_score", int(qp.get("total_score", 0)))
    except ValueError:
        total_score = 0

    # 2) if empty, fallback to last saved analysis on disk
    if (not summary or not matches) and ANALYSIS_PATH.exists():
        with ANALYSIS_PATH.open("r", encoding="utf-8") as f:
            saved = json.load(f)
        policy_text = saved.get("policy_text", "")
        summary = saved.get("summary", "")
        risk_level = saved.get("risk_level", risk_level)
        confidence = saved.get("confidence", confidence)
        total_score = saved.get("total_score", total_score)
        matches = saved.get("matches", {})      # ← LOAD FROM FILE


    if not summary or not matches:
        st.warning("Run an analysis on the Home page first, then come back here to download the report.")
        return

    st.write("")
    st.write("")

    spacer, col1, col2, spacer2 = st.columns([2, 2, 2, 2])
    with col1:
        st.download_button(
            "📥 Download PDF",
            data=generate_pdf_report(policy_text, matches, summary, risk_level, confidence, total_score),
            file_name="TermsBuster_Report.pdf",
            mime="application/pdf"
    )
    with col2:
        st.download_button(
        "🖼️ Download Image",
        data=generate_image_report(policy_text, matches, summary, risk_level, confidence, total_score),
        file_name="TermsBuster_Report.png",
        mime="image/png"
    )

# --- Navigation with query params ---
query_params = st.query_params
active_page = query_params.get("page", "Home")

if "action" in query_params and query_params["action"] == "refresh":
    # clear all params and rerun = hard refresh
    st.query_params.clear()
    st.rerun()

navbar(active_page=active_page)

if active_page == "Home":
    home_page()
elif active_page == "About":
    about_page()
elif active_page == "Download":
    download_page()
else:
    home_page()
