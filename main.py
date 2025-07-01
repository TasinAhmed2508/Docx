import tkinter as tk
from tkinter import messagebox, scrolledtext
from ai_agent import get_python_docx_code, GEMINI_MODEL_LITE, GEMINI_MODEL_FULL
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def show_response_popup(response_text):
    response_window = tk.Toplevel()
    response_window.title("Raw AI Response")
    response_window.geometry("800x600")
    st = scrolledtext.ScrolledText(response_window, wrap=tk.WORD, font=("Consolas", 11))
    st.pack(expand=True, fill='both')
    st.insert(tk.END, response_text)
    st.config(state=tk.DISABLED)
    tk.Button(response_window, text="Close", command=response_window.destroy).pack(pady=10)


def generate_docx_code():
    user_text = text_input.get("1.0", tk.END).strip()
    if not user_text:
        messagebox.showwarning("Input Required", "Please enter some text.")
        return
    try:
        selected_model = model_var.get()
        _, response_text = get_python_docx_code(user_text, model_name=selected_model)
        print("Raw AI response text:\n", response_text)
        if not response_text or not response_text.strip():
            messagebox.showerror("Error", "The AI did not return any response. Please try again with a simpler input or check your API key/quota.")
            return
        # Save response to a file in the project folder
        response_path = os.path.join(PROJECT_DIR, "raw_ai_response.txt")
        with open(response_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        messagebox.showinfo("Saved", f"Raw AI response saved as:\n{response_path}")
        # Show response in a popup window
        show_response_popup(response_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

root = tk.Tk()
root.title("AI Equation to DOCX Generator")
root.geometry("600x450")

label = tk.Label(root, text="Enter your text (with equations):")
label.pack(pady=10)

text_input = tk.Text(root, height=15, width=70)
text_input.pack(padx=10, pady=5)

# Model selection dropdown
model_var = tk.StringVar(value=GEMINI_MODEL_LITE)
model_label = tk.Label(root, text="Select Gemini Model:")
model_label.pack(pady=(10, 0))
model_options = [
    ("Lite (gemini-2.0-flash-lite)", GEMINI_MODEL_LITE),
    ("Full (gemini-2.0-flash-lite)", GEMINI_MODEL_FULL)
]
model_menu = tk.OptionMenu(root, model_var, *[opt[1] for opt in model_options])
model_menu.pack(pady=5)

# Show user-friendly names in dropdown
menu = model_menu["menu"]
menu.delete(0, "end")
for name, value in model_options:
    menu.add_command(label=name, command=lambda v=value: model_var.set(v))

generate_btn = tk.Button(root, text="Get Raw AI Response", command=generate_docx_code)
generate_btn.pack(pady=15)

root.mainloop() 