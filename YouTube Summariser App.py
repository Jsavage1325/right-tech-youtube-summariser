import json
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import keyring
from cryptography.fernet import Fernet

from youtube_summariser import main

def update_stringvar(*args):
    prompt_var.set(prompt_entry.get("1.0", "end-1c"))

def get_encryption_key():
    key = keyring.get_password("YouTubeSummarizerApp", "encryption_key")
    if key is None:
        key = Fernet.generate_key().decode()
        keyring.set_password("YouTubeSummarizerApp", "encryption_key", key)
    return key.encode()

cipher_suite = Fernet(get_encryption_key())

def encrypt_api_key(api_key):
    if api_key:
        return cipher_suite.encrypt(api_key.encode()).decode()
    return ""

def decrypt_api_key(encrypted_api_key):
    if encrypted_api_key:
        return cipher_suite.decrypt(encrypted_api_key.encode()).decode()
    return ""

def get_app_support_path(app_name):
    home = Path.home()
    app_support_path = home / 'Library' / 'Application Support' / app_name
    app_support_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    return app_support_path

# Usage
app_name = 'YouTube Summariser App'
data_path = get_app_support_path(app_name) / 'data.json'
print(data_path)

def save_settings(settings):
    if 'api_key' in settings and settings['api_key']:
        settings['api_key'] = encrypt_api_key(settings['api_key'])
    try:
        print(f'saving settings: {settings}')
        with open(data_path, 'w') as file:
            json.dump(settings, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

def load_settings():
    try:
        if data_path.exists():
            with open(data_path, 'r') as file:
                settings = json.load(file)
                if 'api_key' in settings:
                    settings['api_key'] = decrypt_api_key(settings['api_key'])
                return settings
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
        return {}

def run_script(video_urls, model, prompt, output_path, api_key):
    try:
        main(video_urls, prompt, False, model, output_path, api_key)
        messagebox.showinfo("Success", "Processing complete!")
    finally:
        processing_label.config(text="")  # Clear the processing message
        process_button.config(state=tk.NORMAL)  # Re-enable the button

def start_processing():
    input_file_path = input_file_path_var.get()
    if not input_file_path:
        messagebox.showwarning("Warning", "Please select an input file.")
        return

    output_path = output_path_var.get()
    if not output_path:
        messagebox.showwarning("Warning", "Please select an output path.")
        return

    api_key = api_key_var.get()
    if not api_key:
        messagebox.showwarning("Warning", "Please enter your API key.")
        return

    try:
        with open(input_file_path, 'r') as file:
            video_urls = file.read().splitlines()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {str(e)}")
        return

    model = model_var.get()
    prompt = prompt_var.get()
    process_button.config(state=tk.DISABLED)  # Disable the button during processing
    processing_label.config(text="Processing...")
    threading.Thread(target=run_script, args=(video_urls, model, prompt, output_path, api_key)).start()

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        input_file_path_var.set(file_path)
        input_file_label.config(text=f"Input File: {file_path}")

def select_output_path():
    path = filedialog.askdirectory()
    if path:
        output_path_var.set(path)
        output_path_label.config(text=f"Output Path: {path}")

app = tk.Tk()
app.title("YouTube Video Summarizer")
app.geometry("550x550")  # Set initial size
app.minsize(400, 350)  # Set minimum size

def on_app_close():
    settings = {
        'input_file_path': input_file_path_var.get(),
        'output_path': output_path_var.get(),
        'api_key': api_key_var.get(),
        'prompt': prompt_var.get(),
        'model': model_var.get()
    }
    save_settings(settings)
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_app_close)

# Input File Selection
input_file_path_var = tk.StringVar()
input_file_label = tk.Label(app, text="No input file selected.")
input_file_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
select_input_file_button = tk.Button(app, text="Select Input File", command=select_input_file)
select_input_file_button.grid(row=1, column=0, padx=10, pady=5)

# Output Path Selection
output_path_var = tk.StringVar()
output_path_label = tk.Label(app, text="No output path selected.")
output_path_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
path_label = tk.Button(app, text="Select Output Path", command=select_output_path)
path_label.grid(row=3, column=0, padx=10, pady=5)

# API Key Entry
api_key_var = tk.StringVar()
api_key_label = tk.Label(app, text="Enter API Key:")
api_key_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
api_key_entry = tk.Entry(app, textvariable=api_key_var, show="*")
api_key_entry.grid(row=5, column=0, padx=10, pady=5)

# Prompt Entry
prompt_var = tk.StringVar()
prompt_var.trace("w", lambda name, index, mode: prompt_entry.delete("1.0", "end") or prompt_entry.insert("1.0", prompt_var.get()))

prompt_label = tk.Label(app, text="Prompt")
prompt_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

# prompt_entry = tk.Entry(app, textvariable=prompt_var)
prompt_entry = tk.Text(app, height=5, width=60)
prompt_entry.grid(row=7, column=0, padx=10, pady=5)

prompt_entry.bind("<KeyRelease>", lambda event: update_stringvar())

# Model Selection
model_var = tk.StringVar(value="haiku")
model_label = tk.Label(app, text="Choose Model:")
model_label.grid(row=8, column=0, padx=10, pady=5)
model_dropdown = tk.OptionMenu(app, model_var, "haiku", "sonnet", "opus")
model_dropdown.grid(row=9, column=0, padx=10, pady=5)

# Processing Message
processing_label = tk.Label(app, text="")
processing_label.grid(row=10, column=0, padx=10, pady=5)

# Start Processing Button
process_button = tk.Button(app, text="Start Processing", command=start_processing)
process_button.grid(row=11, column=0, padx=10, pady=10)

# Quit Button
quit_button = tk.Button(app, text="Quit", command=app.quit)
quit_button.grid(row=12, column=0, padx=10, pady=10)

# Load settings at startup
settings = load_settings()
input_file_path_var.set(settings.get('input_file_path', ''))
output_path_var.set(settings.get('output_path', ''))
api_key_var.set(settings.get('api_key', ''))
prompt_var.set(settings.get('prompt', ''))
model_var.set(settings.get('model', 'haiku'))

if input_file_path_var.get():
    input_file_label.config(text=f"Input File: {input_file_path_var.get()}")
if output_path_var.get():
    output_path_label.config(text=f"Output Path: {output_path_var.get()}")

app.mainloop()
