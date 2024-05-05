import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, Radiobutton
from tkinter import filedialog

from youtube_summariser import main


def run_script(video_urls, should_save_transcript, model):
    try:
        main(video_urls, should_save_transcript, model)
        messagebox.showinfo("Success", "Processing complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def start_processing():
    urls = text_area.get('1.0', tk.END).splitlines()
    should_save = save_transcript_var.get()
    model = model_var.get()
    threading.Thread(target=run_script, args=(urls, should_save, model)).start()

def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {str(e)}")
        return []

def select_output_path():
    path = filedialog.askdirectory()
    if path:
        output_path_var.set(path)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_var.set(file_path)
        file_path_label.config(text=f"Selected File: {file_path}")


app = tk.Tk()
app.title("YouTube Video Summarizer")

input_method_var = tk.StringVar(value="URLs")

# Text area for input
url_label = tk.Label(app, text="Select File Containing YouTube Urls:")
url_label.pack()

# File selection
file_path_var = tk.StringVar()
file_path_label = tk.Label(app, text="No file selected.")
select_file_button = tk.Button(app, text="Select File", command=select_file)
select_file_button.pack()

# Option for model selection
model_var = tk.StringVar(value="haiku")
model_label = tk.Label(app, text="Choose Model:")
model_label.pack()
model_dropdown = tk.OptionMenu(app, model_var, "haiku", "sonnet", "opus")
model_dropdown.pack()

# Path selection and display
output_path_var = tk.StringVar()
path_label = tk.Button(app, text="Select Output Path", command=select_output_path)
path_label.pack(pady=10)
output_path_label = tk.Label(app, text="No output path selected.")
output_path_label.pack()

# Button to start processing
process_button = tk.Button(app, text="Start Processing", command=start_processing)
process_button.pack(pady=20)

# Quit button
quit_button = tk.Button(app, text="Quit", command=app.quit)
quit_button.pack(pady=5)

app.mainloop()
