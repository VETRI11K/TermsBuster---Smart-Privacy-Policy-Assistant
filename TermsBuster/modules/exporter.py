# modules/exporter.py
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


# ---------- Helper functions ----------

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width (for PIL drawing)."""
    from PIL import ImageDraw, Image

    if not text:
        return []

    words = text.split()
    lines = []
    current_line = []

    # temp drawing context just to measure
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines


def get_risk_color(level_key: str) -> str:
    """Return a color hex based on risk level key."""
    k = (level_key or "").lower()
    if "very_high" in k:
        return "#ff4444"
    if "high" in k:
        return "#ff8844"
    if "moderate" in k:
        return "#ffbb33"
    return "#44ff88"  # low / minimal


# ---------- PDF REPORT ----------

def generate_pdf_report(policy_text, matches, summary, risk_level, confidence, total_score):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#158cff',
        spaceAfter=30,
        alignment=1,
    )

    # Title
    story.append(Paragraph("TermsBuster - Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Summary: " + (summary or ""), styles['BodyText']))
    story.append(Spacer(1, 12))

    # Scores
    story.append(Paragraph(f"Risk Level: {risk_level}", styles['BodyText']))
    story.append(Paragraph(f"Confidence: {confidence}/100", styles['BodyText']))
    story.append(Paragraph(f"Total Score: {total_score}", styles['BodyText']))
    story.append(Spacer(1, 8))

    # Dynamic recommendation (no policy preview)
    lev = (risk_level or "").lower()
    ts = total_score or 0

    if "very high" in lev or ts >= 180:
        advice_text = (
            "Recommendation: Very high privacy risk. Avoid using this service for any "
            "sensitive or personal data."
        )
    elif "high" in lev or ts >= 160:
        advice_text = (
            "Recommendation: High privacy risk. Do not share highly sensitive data such as "
            "ID numbers, bank details, or health information."
        )
    elif "moderate" in lev or ts >= 120:
        advice_text = (
            "Recommendation: Moderate risk. Review settings, limit optional data sharing, "
            "and disable personalised ads if possible."
        )
    elif "low" in lev or ts >= 50:
        advice_text = (
            "Recommendation: Low risk. Basic practices are acceptable, but still review "
            "permissions before sharing extra data."
        )
    else:
        advice_text = (
            "Recommendation: No major risk detected, but read important sections before "
            "sharing personal information."
        )

    story.append(Paragraph(advice_text, styles['BodyText']))
    story.append(Spacer(1, 16))

    # Matched keywords & sentences
    story.append(Paragraph("Matched Keywords & Sentences:", styles['Heading2']))
    story.append(Spacer(1, 8))

    if not matches:
        story.append(Paragraph("No keyword matches were detected in this policy.", styles['BodyText']))
    else:
        for level_key, level_data in matches.items():
            if not level_data:
                continue
            for kw, detail in level_data.items():
                sentences = detail.get("sentences", [])
                if not sentences:
                    continue
                story.append(Paragraph(
                    f"{kw} ({level_key.replace('_', ' ').title()})",
                    styles['BodyText'],
                ))
                for sent in sentences:
                    story.append(Paragraph(f"- {sent}", styles['BodyText']))
                story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ---------- IMAGE REPORT ----------

def generate_image_report(policy_text, matches, summary, risk_level, confidence, total_score):
    from PIL import Image, ImageDraw, ImageFont
    img_width, img_height = 1400, 1000
    img = Image.new('RGB', (img_width, img_height), color='#020617')
    d = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        heading_font = ImageFont.truetype("arial.ttf", 28)
        subheading_font = ImageFont.truetype("arial.ttf", 22)
        body_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        title_font = heading_font = subheading_font = body_font = small_font = ImageFont.load_default()

    y_pos = 60
    margin = 60
    line_height = 32
    section_gap = 40

    # Title
    d.text((margin, y_pos), "TermsBuster - Analysis Report", fill='#3db8f6', font=title_font)
    y_pos += 70

    # Separator
    d.line([(margin, y_pos), (img_width - margin, y_pos)], fill='#374151', width=2)
    y_pos += 40

    # Metrics
    d.text((margin, y_pos), f"Risk Level: {risk_level}", fill="#ffe56b", font=heading_font)
    y_pos += line_height + 16
    d.text((margin, y_pos), f"Confidence: {confidence}/100", fill="#10b981", font=heading_font)
    y_pos += line_height + 16
    d.text((margin, y_pos), f"Total Score: {total_score}", fill="#ff6b6b", font=heading_font)
    y_pos += section_gap + 20

    # Summary
    d.text((margin, y_pos), "Summary:", fill="#e5e7eb", font=heading_font)
    y_pos += line_height + 16
    summary_text = (summary or "")[:500]
    wrapped_summary = wrap_text(summary_text, body_font, img_width - 2 * margin - 40)
    for line in wrapped_summary[:6]:
        d.text((margin + 40, y_pos), line, fill="#d1d5db", font=body_font)
        y_pos += line_height + 8
    y_pos += section_gap

    # Matched keywords
    d.text((margin, y_pos), "Matched Keywords & Sentences:", fill="#e5e7eb", font=heading_font)
    y_pos += line_height + 20

    if not matches:
        d.text((margin + 40, y_pos), "No keyword matches detected.", fill="#9ca3af", font=body_font)
        y_pos += line_height
    else:
        for level_key, level_data in matches.items():
            if not level_data:
                continue
            for kw, detail in level_data.items():
                sentences = detail.get("sentences", [])
                if not sentences:
                    continue

                risk_color = get_risk_color(level_key)
                keyword_text = f"► {kw.upper()}"
                d.text((margin + 40, y_pos), keyword_text, fill=risk_color, font=subheading_font)
                y_pos += line_height + 8

                risk_label = level_key.replace('_', ' ').title()
                d.text((margin + 60, y_pos), f"Risk: {risk_label}", fill=risk_color, font=small_font)
                y_pos += line_height

                for i, sent in enumerate(sentences[:2]):  # max 2 per keyword
                    wrapped_sent = wrap_text(sent, small_font, img_width - 2 * margin - 80)
                    for line in wrapped_sent[:2]:  # max 2 lines per sentence
                        d.text((margin + 80, y_pos), line, fill="#b0b8c0", font=small_font)
                        y_pos += line_height - 6
                    y_pos += 8

                y_pos += 16
                if y_pos > img_height - 160:
                    break  # avoid drawing below canvas
            if y_pos > img_height - 160:
                break

    # Dynamic recommendation at bottom if there is space
    if y_pos < img_height - 120:
        lev = (risk_level or "").lower()
        ts = total_score or 0

        if "very high" in lev or ts >= 180:
            rec = "Very high risk: avoid using this service for any sensitive or personal data."
        elif "high" in lev or ts >= 160:
            rec = "High risk: do not share ID numbers, bank details, or health data."
        elif "moderate" in lev or ts >= 120:
            rec = "Moderate risk: review settings and limit optional data sharing."
        elif "low" in lev or ts >= 50:
            rec = "Low risk: still review permissions before sharing extra data."
        else:
            rec = "No major risk: stay informed and watch for future policy changes."

        d.text((margin, img_height - 110), "Recommendation:", fill="#e5e7eb", font=heading_font)
        rec_lines = wrap_text(rec, small_font, img_width - 2 * margin)
        y_rec = img_height - 80
        for line in rec_lines[:3]:
            d.text((margin, y_rec), line, fill="#d1d5db", font=small_font)
            y_rec += line_height - 6

    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer
