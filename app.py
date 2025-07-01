from flask import Flask, request, jsonify, send_from_directory
import os
import traceback

from ai_agent import get_python_docx_code

app = Flask(__name__)

# Configuration
GENERATED_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_files")
os.makedirs(GENERATED_FILES_DIR, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html') # Assuming index.html will be in the root

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        user_text = data.get('text')
        if not user_text:
            return jsonify({"error": "Input text is required."}), 400

        # Step 1: Get Python code from AI
        # For now, we'll use the LITE model. Model selection can be added later.
        ai_python_code, raw_ai_response = get_python_docx_code(user_text)

        if not ai_python_code or not ai_python_code.strip():
            return jsonify({
                "error": "The AI did not return any Python code.",
                "raw_ai_response": raw_ai_response
            }), 500

        # Step 2: Execute the AI-generated Python code
        # WARNING: Executing code from an external source like an AI can be risky.
        # Ensure the AI's prompt is robustly designed to prevent malicious code generation.
        # The AI is prompted to save the file as 'output.docx'.
        # We'll execute it in a context where 'output.docx' is saved to GENERATED_FILES_DIR.

        output_filename = "output.docx"
        full_output_path = os.path.join(GENERATED_FILES_DIR, output_filename)

        # Create a dictionary for the global and local scope of exec
        # This allows the executed code to "see" necessary variables, like full_output_path
        # and also allows us to retrieve variables set by the executed code if needed.
        exec_globals = {
            "__builtins__": __builtins__,
            "os": os, # Make os module available if AI code needs it for paths
            # Potentially add 'Document' and 'math2docx' if AI code assumes they are imported
            # However, the prompt asks the AI to include imports in its generated code.
            # Let's assume AI generates full script with imports.
        }

        # Change CWD for exec so 'output.docx' is saved in the right place by the AI's code
        original_cwd = os.getcwd()
        os.chdir(GENERATED_FILES_DIR)
        try:
            exec(ai_python_code, exec_globals)
            # Check if the file was created
            if not os.path.exists(output_filename): # AI code should save as 'output.docx'
                 # Fallback if AI saves to a different name (less ideal)
                generated_doc_files = [f for f in os.listdir('.') if f.endswith('.docx')]
                if generated_doc_files:
                    # If multiple, pick the first one. This is a simple heuristic.
                    os.rename(generated_doc_files[0], output_filename)
                else:
                    raise FileNotFoundError("AI code executed but 'output.docx' was not found in generated_files directory.")
        except Exception as e:
            os.chdir(original_cwd) # Important to change back CWD
            return jsonify({
                "error": f"Error executing AI-generated code: {str(e)}",
                "raw_ai_response": ai_python_code,
                "traceback": traceback.format_exc()
            }), 500
        finally:
            os.chdir(original_cwd) # Ensure CWD is always restored

        return jsonify({
            "message": "DOCX generation process initiated.",
            "raw_ai_response": ai_python_code,
            "download_url": f"/download/{output_filename}"
        })

    except Exception as e:
        return jsonify({
            "error": f"An unexpected error occurred: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(GENERATED_FILES_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404

if __name__ == '__main__':
    # Note: For development, Flask's built-in server is fine.
    # For production, use a proper WSGI server like Gunicorn.
    app.run(debug=True, port=5001) # Using port 5001 to avoid common conflicts
