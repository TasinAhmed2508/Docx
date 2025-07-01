import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not set in environment or .env file.")

GEMINI_MODEL_LITE = 'gemini-2.0-flash-lite'
GEMINI_MODEL_FULL = 'gemini-2.0-flash-lite'  # Only one model used as per user request

def get_python_docx_code(text, model_name=GEMINI_MODEL_LITE):
    """
    Prompts Gemini to return Python code that uses python-docx and math2docx to generate a DOCX file from the input text.
    Supports math, chemistry, physics, and other scientific equations. Instructs the AI to use proper formatting, line spacing, and a beautiful document structure.
    Ensures correct usage of math2docx: always create a paragraph with document.add_paragraph(), then call math2docx.add_math(paragraph, r'...'). Do not use add_math(document, ...), do not use line_spacing with add_math, and do not pass extra arguments to add_math.
    Returns a tuple: (code, raw_response_text).
    """
    genai.configure(api_key=GEMINI_API_KEY)
    prompt = (
        "Convert the following scientific problem and its solution (may include math, chemistry, physics, or other scientific equations) into a Python script that uses the 'python-docx' and 'math2docx' libraries to generate a DOCX file. "
        "Use Document() from python-docx to create the document. "
        "For each equation, first create a paragraph with 'paragraph = document.add_paragraph()', then call 'math2docx.add_math(paragraph, r\"...\")'. "
        "Do not use 'add_math(document, ...)', do not use 'line_spacing' with add_math, and do not pass extra arguments to add_math. "
        "Use add_paragraph() for explanations. "
        "Ensure proper formatting: use line spacing, section headings, and clear separation between steps. "
        "Make the document beautiful and easy to read, with appropriate spacing and structure. "
        "Save the file as 'output.docx'. "
        "Return only the Python code, no explanations or markdown.\n"
        "Here is the input text:\n"
        f"{text}"
    )
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    print("Raw AI response object:", response)
    raw_response_text = getattr(response, 'text', None)
    print("Raw AI response text:", raw_response_text)
    # Remove any accidental markdown code block markers
    code = raw_response_text.strip() if raw_response_text else ''
    if code.startswith('```'):
        code = code.split('```')[-1].strip()
    return code, raw_response_text 