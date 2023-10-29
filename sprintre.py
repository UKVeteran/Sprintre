import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
from docx import Document

class SprintReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprint Reader")

        self.text = tk.Text(self.root, wrap=tk.WORD, height=10, width=40, bg='black', fg='white', font=("TkDefaultFont", 32))
        self.text.pack(pady=10, padx=10)

        self.text.tag_configure('center', justify='center')
        self.text.tag_configure('middle_letter', foreground='blue')  # Change highlight color to blue

        self.start_button = tk.Button(self.root, text="Start", command=self.start_reading, width=20, height=2, font=("Arial", 20))
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_reading, state=tk.DISABLED, width=20, height=2, font=("Arial", 20))
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_reading, state=tk.DISABLED, width=20, height=2, font=("Arial", 20))
        self.resume_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.speed_label = tk.Label(self.root, text="Speed (words per minute):", font=("Arial", 20))
        self.speed_label.pack()

        self.speed_slider = tk.Scale(self.root, from_=100, to=1000, orient=tk.HORIZONTAL)
        self.speed_slider.set(400)  # Initial speed
        self.speed_slider.pack()

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file, width=20, height=2, font=("Arial", 20))
        self.upload_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.highlight_color_label = tk.Label(self.root, text="Highlight Color:", font=("Arial", 20))  # Fix the label text
        self.highlight_color_label.pack()

        self.highlight_color = tk.StringVar()
        self.highlight_color.set('blue')  # Change the default highlight color to blue

        self.color_radio_blue = tk.Radiobutton(self.root, text="Blue", variable=self.highlight_color, value='blue', font=("Arial", 18))
        self.color_radio_blue.pack(anchor=tk.W)

        self.color_radio_red = tk.Radiobutton(self.root, text="Red", variable=self.highlight_color, value='red', font=("Arial", 18))
        self.color_radio_red.pack(anchor=tk.W)

        self.file_path = None
        self.reading = False
        self.pause = False
        self.words = []
        self.index = 0
        self.after_id = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("Word files", "*.docx")])
        if file_path:
            self.file_path = file_path
            self.text.delete("1.0", tk.END)

            if file_path.endswith(".pdf"):
                pdf_reader = PdfReader(file_path)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                self.text.insert(tk.END, text_content)
                self.words = text_content.split()
            elif file_path.endswith((".txt", ".docx")):
                if file_path.endswith(".txt"):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text_content = file.read()
                elif file_path.endswith(".docx"):
                    doc = Document(file_path)
                    text_content = " ".join([para.text for para in doc.paragraphs])
                self.text.insert(tk.END, text_content)
                self.words = text_content.split()

    def start_reading(self):
        if not self.reading:
            self.reading = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.read_word()

    def pause_reading(self):
        if self.reading and not self.pause:
            self.pause = True
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            if self.after_id:
                self.root.after_cancel(self.after_id)

    def resume_reading(self):
        if self.reading and self.pause:
            self.pause = False
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.read_word()

    def read_word(self):
        if self.reading and self.index < len(self.words):
            newlines = "\n" * 5
            word = self.words[self.index]
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, newlines + word)
            self.text.tag_add('center', '1.0', 'end')

            word_len = len(self.words[self.index])
            middle = word_len // 2
            red_letter = f"6.{middle - 1}"
            stop_point = f"6.{middle + 1}"
            self.text.tag_add('middle_letter', red_letter, stop_point)
            self.text.tag_configure('middle_letter', foreground=self.highlight_color.get())

            self.index += 1
            if not self.pause:
                self.after_id = self.root.after(int(60000 / self.speed_slider.get()), self.read_word)
        else:
            self.reading = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = SprintReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
