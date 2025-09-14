# Helper functions

# List of banned words (expand as needed)
BAD_WORDS = ["sex", "fuck", "offensiveword"]

def contains_bad_words(text: str) -> bool:
    """
    Checks if user input contains inappropriate words.
    """
    text_lower = text.lower()
    return any(bad_word in text_lower for bad_word in BAD_WORDS)

def extract_allowed_content(knowledge_source: str) -> str:
    """
    Extracts context from the provided knowledge source.
    (Currently just returns the text, can be extended for OCR/docs.)
    """
    return knowledge_source.strip()
