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
