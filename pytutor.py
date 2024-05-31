import tkinter as tk
from tkinter import scrolledtext, simpledialog
import re
import json

# Admin password for adding new concepts
ADMIN_PASSWORD = "password"
# Filename for storing concepts
CONCEPTS_FILENAME = 'concepts.json'

# Function to load existing concepts from a JSON file
def load_concepts(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save updated concepts to a JSON file
def save_concepts(concepts, filename):
    with open(filename, 'w') as file:
        json.dump(concepts, file, indent=4)

# Function to explain a concept
def explain_concept(concepts, concept):
    return concepts.get(concept, "Concept not found. Could you try rephrasing or ask about another concept?")

# Function to provide an example for a concept
def provide_example(concepts, concept):
    return concepts.get(concept + '_example', "Example not found. Could you try rephrasing or ask about another concept?")

# Function to identify a concept in the user's question
def identify_concept(question, concepts):
    for concept in concepts:
        if re.search(rf'\b{concept}\b', question, re.IGNORECASE):
            return concept
    return None

# Function to add a new concept to the knowledge base
def add_concept(concepts):
    def save_new_concept():
        nonlocal concept_entry, explanation_entry, example_entry
        concept = concept_entry.get().strip().lower()
        explanation = explanation_entry.get().strip()
        example = example_entry.get().strip()
        concepts[concept] = explanation
        concepts[concept + '_example'] = example
        save_concepts(concepts, CONCEPTS_FILENAME)  # Save the updated concepts to the JSON file
        update_chat_history(f"Concept '{concept}' has been added successfully!")
        dialog_window.destroy()

    def authenticate_admin():
        password = simpledialog.askstring("Admin Authentication", "Enter admin password:", show='*')
        if password == ADMIN_PASSWORD:
            save_new_concept()
        else:
            update_chat_history("Incorrect password. Please try again.")

    dialog_window = tk.Toplevel(root)
    dialog_window.title("Add New Concept")

    concept_label = tk.Label(dialog_window, text="Concept Name:")
    concept_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    concept_entry = tk.Entry(dialog_window)
    concept_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    explanation_label = tk.Label(dialog_window, text="Explanation:")
    explanation_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    explanation_entry = tk.Entry(dialog_window)
    explanation_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    example_label = tk.Label(dialog_window, text="Example:")
    example_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    example_entry = tk.Entry(dialog_window)
    example_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    add_button = tk.Button(dialog_window, text="Add Concept", command=authenticate_admin)
    add_button.grid(row=3, columnspan=2, padx=10, pady=10, sticky="ew")

    dialog_window.transient(root)
    dialog_window.grab_set()
    root.wait_window(dialog_window)

def update_chat_history(message):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, message + "\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)

def process_input(event=None):
    user_question = user_input.get().strip()
    user_input.delete(0, tk.END)
    if user_question.lower() == 'exit':
        update_chat_history("Goodbye! Happy coding!")
        root.quit()
    elif user_question.lower() == 'add':
        add_concept(concepts)
    else:
        concept = identify_concept(user_question, concepts)
        if concept:
            explanation = explain_concept(concepts, concept)
            example = provide_example(concepts, concept)
            update_chat_history(f"\n🔍 Explanation of {concept}:\n{explanation}\n\n💡 Example of {concept}:\n{example}")
        else:
            update_chat_history("Hmm, I didn't quite catch that. Could you ask about another concept or rephrase your question? 🤔")

root = tk.Tk()
root.title("Python Tutor Bot")

concepts = load_concepts(CONCEPTS_FILENAME)

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

user_input = tk.Entry(root)
user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
user_input.bind("<Return>", process_input)

add_concept_button = tk.Button(root, text="Add New Concept", command=lambda: add_concept(concepts))
add_concept_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

update_chat_history("Hello! I'm your Python tutor bot.\n")
update_chat_history("You can ask me about these concepts: print, for, while, if, variables, lists, functions, strings, dictionaries, tuples, sets, input, comments, operators, import")
update_chat_history("You can also add new concepts by typing 'add' (admin access required).\n")

root.mainloop()