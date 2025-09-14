import os
import google.generativeai as genai
from dotenv import load_dotenv
from rules import SYSTEM_PROMPT
from utils import contains_bad_words, extract_allowed_content

load_dotenv()
# Load Gemini API key (set as environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def chatbot_response(user_input, knowledge_source):
    """
    Generates chatbot response following strict rules and constraints.
    """
    # 1. Check for bad words
    if contains_bad_words(user_input):
        return "⚠️ Sorry, I cannot respond to inappropriate content."

    # 2. Extract allowed context from knowledge source
    context = extract_allowed_content(knowledge_source)

    # 3. Build system + user prompt
    full_prompt = f"""{SYSTEM_PROMPT}

Knowledge Source:
{context}

User Question:
{user_input}
"""

    # 4. Generate response
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
