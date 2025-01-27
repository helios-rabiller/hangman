import pygame
import random
import os
import json

# Pygame Initialization
pygame.init()

# Window settings
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)

# Fonts
if not os.path.exists("Nosifer-Regular.ttf"):  # Check if the font exists
    print("The font 'Nosifer-Regular.ttf' is missing")
    exit()
main_font = pygame.font.Font("Nosifer-Regular.ttf", 72)  # Specify the custom font
font = pygame.font.Font(None, 36)

# Files
WORDS_FILE = "words.txt"
SCORES_FILE = "scores.json"
MUSIC_FILE = "song257345.mp3"  # Ensure this file is in the same folder as your script

# File verification
if not os.path.exists(WORDS_FILE):
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        f.write("python\npygame\nprogramming\nhangman\nvariable\nloop\ndeveloper\n")

if not os.path.exists(SCORES_FILE):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)  # Create an empty JSON file if it doesn't exist

# Load words
def load_words(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [word.strip().upper() for word in f.readlines()]

# Separate words by difficulty
def get_words_by_difficulty(words, level="easy"):
    if level == "easy":
        return [word for word in words if len(word) <= 6]
    elif level == "hard":
        return [word for word in words if len(word) >= 7]

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

# Draw the hangman
def draw_hangman(mistakes):
    if mistakes > 0:
        pygame.draw.line(screen, BLACK, (100, HEIGHT - 150), (300, HEIGHT - 150), 5)  # Base
    if mistakes > 1:
        pygame.draw.line(screen, BLACK, (200, HEIGHT - 150), (200, 100), 5)  # Pole
    if mistakes > 2:
        pygame.draw.line(screen, BLACK, (200, 100), (350, 100), 5)  # Beam
    if mistakes > 3:
        pygame.draw.line(screen, BLACK, (350, 100), (350, 150), 5)  # Rope
    if mistakes > 4:
        pygame.draw.circle(screen, BLACK, (350, 180), 30, 5)  # Head
    if mistakes > 5:
        pygame.draw.line(screen, BLACK, (350, 210), (350, 300), 5)  # Body
    if mistakes > 6:
        pygame.draw.line(screen, BLACK, (350, 300), (320, 400), 5)  # Left leg
    if mistakes > 7:
        pygame.draw.line(screen, BLACK, (350, 300), (380, 400), 5)  # Right leg
    if mistakes > 8:
        pygame.draw.line(screen, BLACK, (350, 250), (320, 220), 5)  # Left arm
    if mistakes > 9:
        pygame.draw.line(screen, BLACK, (350, 250), (380, 220), 5)  # Right arm

# Game logic
def play_game(level="easy"):
    words = load_words(WORDS_FILE)
    chosen_word = random.choice(get_words_by_difficulty(words, level))
    guessed_word = ["_"] * len(chosen_word)
    guessed_letters = set()
    wrong_letters = []
    mistakes = 0
    max_mistakes = 7

    running = True
    while running:
        screen.fill(GRAY)

        # Offset to the right
        offset_x = 100

        # Display the word
        word_surface = font.render(" ".join(guessed_word), True, BLACK)
        screen.blit(word_surface, (WIDTH // 2 - word_surface.get_width() // 2 + offset_x, HEIGHT // 4))

        # Display incorrect letters
        wrong_surface = font.render("Errors: " + " ".join(wrong_letters), True, RED)
        screen.blit(wrong_surface, (50, HEIGHT - 100))

        # Draw the hangman under the word
        draw_hangman(mistakes)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    letter = pygame.key.name(event.key).upper()
                    if letter.isalpha() and letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter in chosen_word:
                            for i, l in enumerate(chosen_word):
                                if l == letter:
                                    guessed_word[i] = letter
                        else:
                            if letter not in wrong_letters:
                                wrong_letters.append(letter)
                                mistakes += 1

        # Check for win or loss
        if "_" not in guessed_word:
            save_score(max_mistakes - mistakes)
            running = False
        if mistakes >= max_mistakes:
            running = False

# Save score
def save_score(score):
    screen.fill(GRAY)
    input_surface = font.render("Enter your name: ", True, BLACK)
    screen.blit(input_surface, (50, HEIGHT // 2 - 50))
    pygame.display.flip()

    name = ""
    entering = True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if name.strip():
                        entering = False
                    else:
                        input_surface = font.render("Enter a valid name: ", True, RED)
                        screen.blit(input_surface, (50, HEIGHT // 2 - 50))
                        pygame.display.flip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(GRAY)
        screen.blit(input_surface, (50, HEIGHT // 2 - 50))
        name_surface = font.render(name, True, BLACK)
        screen.blit(name_surface, (50, HEIGHT // 2))
        pygame.display.flip()

    if name:
        history = load_history()
        history.append({"name": name.strip(), "score": score})
        history = sorted(history, key=lambda x: x["score"], reverse=True)
        save_history(history[:10])  # Keep the top 10 scores

# Display score leaderboard
def show_scores():
    screen.fill(GRAY)
    title = font.render("Leaderboard", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    try:
        history = load_history()
        if not history:
            raise ValueError("No entries in the leaderboard.")
        for i, entry in enumerate(history[:10], start=1):  # Top 10
            score_text = font.render(f"{i}. {entry['name']}: {entry['score']}", True, BLACK)
            screen.blit(score_text, (100, 100 + i * 30))
    except Exception as e:
        error_text = font.render(str(e), True, RED)
        screen.blit(error_text, (100, 100))

    # Clear button
    clear_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)
    pygame.draw.rect(screen, DARK_GRAY, clear_button_rect)
    clear_text = font.render("Clear", True, WHITE)
    screen.blit(clear_text, (clear_button_rect.x + (clear_button_rect.width - clear_text.get_width()) // 2, 
                              clear_button_rect.y + (clear_button_rect.height - clear_text.get_height()) // 2))

    # Back button
    back_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 160, 150, 50)
    pygame.draw.rect(screen, DARK_GRAY, back_button_rect)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button_rect.x + (back_button_rect.width - back_text.get_width()) // 2, 
                              back_button_rect.y + (back_button_rect.height - back_text.get_height()) // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clear_button_rect.collidepoint(event.pos):
                    save_history([])  # Clear the scores file
                elif back_button_rect.collidepoint(event.pos):
                    waiting = False  # Return to the main menu

# Main menu
def main_menu():
    running = True
    while running:
        screen.fill(GRAY)
        title = main_font.render("Hangman", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Menu buttons
        buttons = [
            {"text": "Easy Level", "rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 75, 250, 50), "action": lambda: play_game("easy")},
            {"text": "Hard Level", "rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 15, 250, 50), "action": lambda: play_game("hard")},
            {"text": "Leaderboard", "rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 45, 250, 50), "action": show_scores},
            {"text": "Exit", "rect": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 105, 250, 50), "action": exit}
        ]

        for button in buttons:
            pygame.draw.rect(screen, DARK_GRAY, button["rect"])
            text_surface = font.render(button["text"], True, WHITE)
            screen.blit(text_surface, (button["rect"].x + (button["rect"].width - text_surface.get_width()) // 2,
                                       button["rect"].y + (button["rect"].height - text_surface.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game("easy")
                elif event.key == pygame.K_2:
                    play_game("hard")
                elif event.key == pygame.K_3:
                    show_scores()
                elif event.key == pygame.K_4:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    pygame.quit()
    exit()

# Start music
pygame.mixer.music.load(MUSIC_FILE)
pygame.mixer.music.play(-1)  # Play music in a loop

# Start the game
main_menu()