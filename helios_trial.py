import json
import os
import random
import sys
import pygame

pygame.init()

size = width, height = 1200, 940
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hangman Game")
font = pygame.font.Font(None, 48)

word_list_file = "words_data.json"

def load_animation_frames(path, file_format="png"):
    frames = []
    for frame_file in sorted(os.listdir(path), key=lambda x: int(x.split('_')[-1].split('.')[0])):
        if frame_file.endswith(file_format):
            frame_path = os.path.join(path, frame_file)
            frames.append(pygame.image.load(frame_path).convert_alpha())
    return frames

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

# Draw the hangman figure
def draw_hangman(screen, mistakes):
    base_x, base_y = 200, 700
    pole_height = 400
    pole_width = 10

    # Base
    pygame.draw.rect(screen, black, (base_x, base_y, 200, 10))
    # Pole
    pygame.draw.rect(screen, black, (base_x + 90, base_y - pole_height, pole_width, pole_height))
    # Top bar
    pygame.draw.rect(screen, black, (base_x + 90, base_y - pole_height, 100, pole_width))
    # Rope
    pygame.draw.rect(screen, black, (base_x + 180, base_y - pole_height + 10, 2, 50))

    # Draw parts of the hangman based on the number of mistakes Head,Body,Left arm, Right Arm, Left leg, Right leg
    if mistakes > 0:  
        pygame.draw.circle(screen, black, (base_x + 180, base_y - pole_height + 80), 30, 5)
    if mistakes > 1:  
        pygame.draw.line(screen, black, (base_x + 180, base_y - pole_height + 110), 
                         (base_x + 180, base_y - pole_height + 200), 5)
    if mistakes > 2:  
        pygame.draw.line(screen, black, (base_x + 180, base_y - pole_height + 130), 
                         (base_x + 150, base_y - pole_height + 160), 5)
    if mistakes > 3:  
        pygame.draw.line(screen, black, (base_x + 180, base_y - pole_height + 130), 
                         (base_x + 210, base_y - pole_height + 160), 5)
    if mistakes > 4:  
        pygame.draw.line(screen, black, (base_x + 180, base_y - pole_height + 200), 
                         (base_x + 150, base_y - pole_height + 250), 5)
    if mistakes > 5:  
        pygame.draw.line(screen, black, (base_x + 180, base_y - pole_height + 200), 
                         (base_x + 210, base_y - pole_height + 250), 5)

# Function to display the menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(white)

        # Title
        title_surface = font.render("Hangman Game", True, black)
        title_rect = title_surface.get_rect(center=(width // 2, height // 4))
        screen.blit(title_surface, title_rect)

        # Options
        play_surface = font.render("Play", True, black)
        play_rect = play_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(play_surface, play_rect)

        quit_surface = font.render("Quit", True, black)
        quit_rect = quit_surface.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(quit_surface, quit_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    main_game()
                elif quit_rect.collidepoint(event.pos):
                    menu_running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Main game loop
def main_game():
    words = load_words()
    if not words:
        print("No words available to play.")
        return
    
    word = choose_word(words)
    guessed_letters = set()
    mistakes = 0
    max_mistakes = 6
    running = True

    animation_frames = load_animation_frames("animations/")
    animation_index = 0
    animation_speed = 9
    
    while running:
        screen.fill(white)
        
        # Draw hangman figure
        draw_hangman(screen, mistakes)
        animation_index += 1
        if animation_index >= len(animation_frames) * animation_speed:
            animation_index = 0
        current_frame = animation_frames[animation_index // animation_speed]
        screen.blit(current_frame, (400, 200))
    
        # Display the word with guessed letters
        displayed_word = " ".join([letter if letter in guessed_letters else "_" for letter in word])
        word_surface = font.render(displayed_word, True, black)
        screen.blit(word_surface, (400, 200))
        # Display guessed letters
        guessed_surface = font.render(f"Guessed: {', '.join(sorted(guessed_letters))}", True, black)
        screen.blit(guessed_surface, (400, 300))
        
        # Check win/lose conditions
        if mistakes >= max_mistakes:
            lose_surface = font.render("You lost! The word was: " + word, True, red)
            screen.blit(lose_surface, (350, 100))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        elif all(letter in guessed_letters for letter in word):
            win_surface = font.render("You win!", True, red)
            screen.blit(win_surface, (550, 100))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    guess = event.unicode.upper()
                    if guess not in guessed_letters:
                        guessed_letters.add(guess)
                        if guess not in word:
                            mistakes += 1
        pygame.display.flip()

    end_menu()

# Function to display the end menu
def end_menu():
    end_running = True
    while end_running:
        screen.fill(white)

        replay_surface = font.render("Play Again", True, black)
        replay_rect = replay_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(replay_surface, replay_rect)

        quit_surface = font.render("Quit", True, black)
        quit_rect = quit_surface.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(quit_surface, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    main_game()
                elif quit_rect.collidepoint(event.pos):
                    end_running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
