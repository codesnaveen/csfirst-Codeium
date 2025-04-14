import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

# Download necessary NLTK resources (only the first time)
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, reduction_ratio=0.3):
    """
    Basic extractive summarizer using frequency-based sentence scoring.
    :param text: The original large text.
    :param reduction_ratio: The fraction of sentences to include in the summary.
    :return: A summary string.
    """
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    if len(sentences) < 2:
        return text

    # Prepare word frequency distribution
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # Score each sentence
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq[word]

    # Select top sentences for summary
    number_of_sentences = max(1, int(len(sentences) * reduction_ratio))
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary_sentences = sorted(sorted_sentences[:number_of_sentences], key=lambda s: sentences.index(s))
    
    summary = ' '.join(summary_sentences)
    return summary

def load_file():
    """Allows user to load text from a file into the input text field."""
    file = filedialog.askopenfile(mode='r', filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        content = file.read()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, content)

def generate_summary():
    """Generates summary from the input text and displays it in the summary field."""
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Required", "Please paste or load text first!")
        return
    summary = summarize_text(text)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)

# Set up the main GUI window
root = tk.Tk()
root.title("Text Summarization Tool")
root.geometry("800x600")

# Create a frame for input text and controls
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_label = tk.Label(input_frame, text="Input Text:")
input_label.pack(anchor="w")

input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15)
input_text.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

load_button = tk.Button(button_frame, text="Load Text File", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

summarize_button = tk.Button(button_frame, text="Generate Summary", command=generate_summary)
summarize_button.pack(side=tk.LEFT, padx=5)

# Create a field for the summary result
summary_label = tk.Label(root, text="Summary (editable):")
summary_label.pack(anchor="w", padx=10)

summary_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
summary_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Run the GUI application
root.mainloop()
