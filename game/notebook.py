import json  # for JSON serialization

class AlphabetNotebook:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.alphabet_notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No previous notes found. New notes initialized.")
            return {chr(i + ord('A')): "" for i in range(26)}

    def save_notes(self):
        with open(self.filename, "w") as file:
            json.dump(self.alphabet_notes, file, indent=2)

    def add_note(self, letter, content):
        if letter in self.alphabet_notes:
            self.alphabet_notes[letter] = content
            print(f"Note for '{letter}' added.")
            self.save_notes()
        else:
            print(f"Invalid letter '{letter}'. Please enter a letter from A to Z.")

    def view_notes(self):
        print("Alphabet Notes:")
        for letter, content in self.alphabet_notes.items():
            print(f"{letter}. {content}")

    def edit_note(self, letter, new_content):
        if letter in self.alphabet_notes:
            self.alphabet_notes[letter] = new_content
            print(f"Note for '{letter}' edited.")
            self.save_notes()
        else:
            print(f"Invalid letter '{letter}'. Please enter a letter from A to Z.")
