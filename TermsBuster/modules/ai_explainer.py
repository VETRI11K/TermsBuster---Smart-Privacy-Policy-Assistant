import re

# General keyword replacement dictionary for common privacy terms to simple phrases
KEYWORD_REPLACEMENTS = {
    r"\bdata breaches?\b": "when your data gets exposed or stolen",
    r"\bretention\b": "keeping your data",
    r"\bpersonal data\b": "your personal information",
    r"\banalysis\b": "looking at information to improve service",
    r"\buser behavior\b": "how you use the service",
    r"\bprofile\b": "create a user profile",
    r"\bconsent\b": "your permission",
    r"\bprocessing\b": "handling",
    r"\bthird parties\b": "other companies or people",
    r"\bdisclosed\b": "shared",
    r"\bsecurity\b": "protection",
    r"\bmonitoring\b": "watching",
    r"\btracking\b": "following",
}

# Templates for commonly detected policy concepts, extendable
TEMPLATES = [
    (r'personal information.*collected', "We collect personal information needed to provide our services."),
    (r'data retention', "We keep your data only as long as necessary."),
    (r'data breaches?', "There are risks your data could be exposed or stolen."),
    (r'consent', "We ask for your permission before using your data."),
    (r'third parties', "Your information may be shared with other companies."),
    (r'security', "We work to protect your information from unauthorized access."),
    (r'profiling', "We create user profiles to personalize services."),
    (r'tracking', "We track usage to improve the platform."),
    (r'legal consequences', "Using this service may have legal implications you should be aware of."),
]

def clean_and_replace(text: str) -> str:
    """
    Applies keyword replacements to simplify jargon into plain language.
    """
    for pattern, replacement in KEYWORD_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def extract_templates(text: str) -> list:
    """
    Matches known patterns and returns corresponding friendly sentences.
    """
    explanations = []
    for pattern, explanation in TEMPLATES:
        if re.search(pattern, text, re.IGNORECASE):
            explanations.append(explanation)
    return explanations

def split_into_sentences(text: str) -> list:
    """
    Naive sentence splitter based on punctuation.
    """
    # Split on period followed by space or line end
    sentences = re.split(r'\.\s+', text.strip())
    # Clean sentences
    sentences = [s.strip() for s in sentences if s]
    return sentences

def generate_ai_friendly_explanation(policy_text: str) -> str:
    """
    Main function: receives original extracted privacy policy text,
    applies keyword replacements and template expansions,
    and returns human-friendly bullet-point explanations.
    """

    # Step 1: Clean and replace jargon keywords with simple phrases
    cleaned_text = clean_and_replace(policy_text)

    # Step 2: Extract matched template explanations based on policy content
    template_explanations = extract_templates(cleaned_text)

    # Step 3: Split cleaned text into sentences for additional clarity
    sentences = split_into_sentences(cleaned_text)

    # Step 4: Combine unique explanations from templates and sentences
    # Prioritize template explanations to ensure key points are highlighted
    combined_explanations = list(dict.fromkeys(template_explanations))  # Remove duplicates
    combined_explanations.extend(sentences)

    # Remove duplicates and short sentences for clarity
    seen = set()
    final_explanations = []
    for exp in combined_explanations:
        normalized = exp.lower()
        if normalized not in seen and len(exp) > 20:  # Ignore trivial info
            seen.add(normalized)
            # Ensure first char uppercase and trailing period
            exp = exp[0].upper() + exp[1:]
            if not exp.endswith('.'):
                exp += '.'
            final_explanations.append(exp)

    # Format as markdown bullet points
    bullet_points = '\n'.join(f"- {line}" for line in final_explanations)

    return bullet_points


# Example standalone test
if __name__ == "__main__":
    sample_policy_text = (
        "This Privacy Policy explains how your Personal Data is collected, used, and disclosed. "
        "We collect data for analysis and tracking user behavior. "
        "Data retention periods apply to keep data only as necessary. "
        "We may share information with third parties and ask for your consent. "
        "Security measures aim to prevent data breaches."
    )

    print(generate_ai_friendly_explanation(sample_policy_text))
