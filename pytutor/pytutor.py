import re
import json

# Admin password for adding new concepts
ADMIN_PASSWORD = "password"

# Function to load existing concepts from a JSON file
def load_concepts(filename='concepts.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save updated concepts to a JSON file
def save_concepts(concepts, filename='concepts.json'):
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
    # Prompt for admin password
    password = input("Enter the admin password to add a new concept:\n").strip()
    
    if password != ADMIN_PASSWORD:
        print("Incorrect password. Access denied.")
        return
    
    concept = input("Enter the new concept name:\n").strip().lower()
    explanation = input(f"Enter the explanation for {concept}:\n").strip()
    example = input(f"Enter an example for {concept}:\n").strip()
    concepts[concept] = explanation
    concepts[concept + '_example'] = example
    save_concepts(concepts)  # Save the updated concepts to the JSON file
    print(f"Concept '{concept}' has been added successfully!")

# Main function to run the chatbot
def main():
    concepts = load_concepts()  # Load existing concepts from file

    print("Hello! I'm your Python tutor bot.")
    print("You can ask me about these concepts: print, for, while, if, variables, lists, functions, strings, dictionaries, tuples, sets, input, comments, operators, import")
    print("You can also add new concepts by typing 'add' (admin access required).")

    while True:
        user_question = input("\nWhat would you like to learn about? (type 'exit' to quit or 'add' to add a new concept):\n")
        if user_question.lower() == 'exit':
            print("Goodbye! Happy coding!")
            break
        elif user_question.lower() == 'add':
            add_concept(concepts)
        else:
            concept = identify_concept(user_question, concepts)
            if concept:
                explanation = explain_concept(concepts, concept)
                example = provide_example(concepts, concept)
                print(f"\n🔍 Explanation of {concept}:\n{explanation}")
                print(f"💡 Example of {concept}:\n{example}")
            else:
                print("Hmm, I didn't quite catch that. Could you ask about another concept or rephrase your question? 🤔")

if __name__ == "__main__":
    main()
