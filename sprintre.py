import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from docx import Document  
import os

class SprintReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprint Reader")
        
        self.text = tk.Text(self.root, wrap=tk.WORD, height=10, width=40)
        self.text.pack(pady=10, padx=10)
        
        self.start_stop_button = tk.Button(self.root, text="Start", command=self.toggle_start_stop)
        self.start_stop_button.pack(side=tk.LEFT, padx=5)
        
        self.speed_label = tk.Label(self.root, text="Speed (words per minute):")
        self.speed_label.pack()
        
        self.speed_slider = tk.Scale(self.root, from_=100, to=1000, orient=tk.HORIZONTAL)
        self.speed_slider.set(300)  # Initial speed
        self.speed_slider.pack()

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.file_path = None
        self.reading = False
        self.words = []
        self.index = 0
        self.after_id = None
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("Word files", "*.docx")])
        if file_path:
            self.file_path = file_path
            self.text.delete("1.0", tk.END)
            
            # Determine the file type and read accordingly
            if file_path.endswith(".pdf"):
                pdf_reader = PdfReader(file_path)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                self.text.insert(tk.END, text_content)
                self.words = text_content.split()
            elif file_path.endswith((".txt", ".docx")):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                    self.text.insert(tk.END, text_content)
                    self.words = text_content.split()
                
    def toggle_start_stop(self):
        if not self.reading:
            self.reading = True
            self.start_stop_button.config(text="Stop")
            self.read_word()
        else:
            self.reading = False
            self.start_stop_button.config(text="Start")
            if self.after_id:
                self.root.after_cancel(self.after_id)

    def read_word(self):
        if self.reading and self.index < len(self.words):
            word = self.words[self.index]
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, word)
            self.index += 1
            self.after_id = self.root.after(int(60000 / self.speed_slider.get()), self.read_word)
        else:
            self.toggle_start_stop()  # Stop reading when reaching the end

def main():
    root = tk.Tk()
    app = SprintReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
