# AI Equation to DOCX Generator

This project provides a simple GUI tool to convert text (with equations in natural language) into a DOCX file, rendering equations as LaTeX math using the Gemini API and Python.

## Features
- Enter text with embedded equations in natural language.
- Uses Gemini AI to convert equations to LaTeX.
- Generates a DOCX file with equations rendered as math.
- Simple GUI (Tkinter).

## Requirements
- Python 3.8+
- `google-generativeai`
- `python-docx`
- `math2docx`
- (Tkinter is included with Python)

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Gemini API key:**
   - Get your API key from Google.
   - Set it as an environment variable:
     - On Windows (PowerShell):
       ```powershell
       $env:GEMINI_API_KEY="your_api_key_here"
       ```
     - On Linux/macOS:
       ```bash
       export GEMINI_API_KEY="your_api_key_here"
       ```

## Usage
1. Run the app:
   ```bash
   python main.py
   ```
2. Enter your text (with equations) in the GUI.
3. Click **Generate DOCX** and choose where to save the file.
4. Open the generated DOCX file in Microsoft Word or compatible editor.

## File Structure
- `main.py` — Launches the GUI and coordinates the workflow.
- `ai_agent.py` — Handles Gemini API and text-to-LaTeX conversion.
- `docx_writer.py` — Writes the DOCX file with math rendering.

## Notes
- The Gemini API may have usage limits or require billing.
- For best results, write equations clearly in your input text. 