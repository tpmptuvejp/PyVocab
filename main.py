import tkinter as tk
from tkinter import scrolledtext, simpledialog, ttk
import re
import json

ADMIN_PASSWORD = "password"
CONCEPTS_FILENAME = 'concepts.json'

# load concepts from JSON
def load_concepts(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# save concepts to JSON
def save_concepts(concepts, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(concepts, file, indent=4)
    except IOError as e:
        update_chat_history(f"Error saving concepts: {e}", "error")

# explain concept
def explain_concept(concepts, concept):
    return concepts.get(concept, "Concept not found. Could you try rephrasing or ask about another concept?")

# example for concept
def provide_example(concepts, concept):
    return concepts.get(concept + '_example', "Example not found. Could you try rephrasing or ask about another concept?")

# identify concept in question
def identify_concept(question, concepts):
    for concept in concepts:
        if re.search(rf'\b{re.escape(concept)}\b', question, re.IGNORECASE):
            return concept
    return None

# add concept to JSON
def add_concept(concepts):
    def save_new_concept():
        concept = concept_entry.get().strip().lower()
        explanation = explanation_entry.get().strip()
        example = example_entry.get().strip()
        password = password_entry.get().strip()

        if not concept or not explanation or not example:
            update_chat_history("All fields are required to add a new concept.", "error")
            return

        if password != ADMIN_PASSWORD:
            update_chat_history("Incorrect password. Please try again.", "error")
            return

        concepts[concept] = explanation
        concepts[f"{concept}_example"] = example
        save_concepts(concepts, CONCEPTS_FILENAME)
        update_chat_history(f"Concept '{concept}' has been added successfully!", "response")
        dialog_window.destroy()

    # add concept UI
    dialog_window = tk.Toplevel(root)
    dialog_window.title("Add New Concept")

    tk.Label(dialog_window, text="Concept Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    concept_entry = tk.Entry(dialog_window)
    concept_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(dialog_window, text="Explanation:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    explanation_entry = tk.Entry(dialog_window)
    explanation_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(dialog_window, text="Example:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    example_entry = tk.Entry(dialog_window)
    example_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(dialog_window, text="Admin Password:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    password_entry = tk.Entry(dialog_window, show='*')
    password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    tk.Button(dialog_window, text="Add Concept", command=save_new_concept).grid(row=4, columnspan=2, padx=10, pady=10, sticky="ew")

    dialog_window.transient(root)
    dialog_window.grab_set()
    root.wait_window(dialog_window)

def update_chat_history(message, tag):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + "\n\n", tag)
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

def process_input(event=None):
    user_question = user_input.get().strip()
    user_input.delete(0, tk.END)
    if user_question.lower() == 'exit':
        update_chat_history("Goodbye! Happy coding!", "response")
        root.quit()
    else:
        update_chat_history(f"You: {user_question}", "user")
        concept = identify_concept(user_question, concepts)
        if concept:
            explanation = explain_concept(concepts, concept)
            example = provide_example(concepts, concept)
            update_chat_history(f"\nExplanation of {concept}:\n{explanation}\n\nExample of {concept}:\n{example}", "response")
        else:
            update_chat_history("Hmm, I didn't quite catch that. Could you check your spelling just to make sure it is correct, or perhaps add a new concept?", "response")

def clear_placeholder(event):
    if user_input.get() == "Type concepts here":
        user_input.delete(0, tk.END)
        user_input.config(fg='white')

def restore_placeholder(event):
    if not user_input.get():
        user_input.config(fg='dark grey')
        user_input.insert(0, "Type concepts here")

# main UI
root = tk.Tk()
root.title("WordPy")
root.resizable(False, False)

concepts = load_concepts(CONCEPTS_FILENAME)

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="black", fg="white")
chat_history.tag_config('user', justify='right', foreground='white')
chat_history.tag_config('response', justify='left', foreground='white')
chat_history.tag_config('error', justify='left', foreground='red')
chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

separator = ttk.Separator(root, orient='horizontal')
separator.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

user_input = tk.Entry(root, fg='dark grey')
user_input.insert(0, "Type concepts here")
user_input.bind("<FocusIn>", clear_placeholder)
user_input.bind("<FocusOut>", restore_placeholder)
user_input.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
user_input.bind("<Return>", process_input)

add_concept_button = tk.Button(root, text="Add New Concept", command=lambda: add_concept(concepts))
add_concept_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

update_chat_history("Hello! I am WordPy, the Python open-source concepts dictionary.", "response")
update_chat_history("You can ask me about Python concepts you don't understand, and I'll try to help.", "response")
update_chat_history("You can also add new concepts by clicking the button below this text window.", "response")
update_chat_history("=" * 80, "response")

root.mainloop()