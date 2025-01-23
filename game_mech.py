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