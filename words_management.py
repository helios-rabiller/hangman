# Function to load words from JSON file
def load_words():
    if os.path.exists(word_list_file):
        with open(word_list_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: The word list file is corrupted.")
                return []
    return []

# Function to choose a random word
def choose_word(words):
    return random.choice(words).upper()
