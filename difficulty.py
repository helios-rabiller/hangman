# Load score history from a JSON file
def load_history():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: The scores file is corrupted. Scores will be reset.")
                return []
    return []

# Save score history to a JSON file
def save_history(history):
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)