# V2 en français

import pygame
import random
import os

def lire_mots(fichier):
    # Lit les mots du fichier et retourne une liste.#
    if not os.path.exists(fichier):
        with open(fichier, 'w') as f:
            f.write("pomme\nbanane\ncerise\norange\nmangue\nraisin\npoire\nfraise\nprune\nkiwi\ncitron\ngoyave\npapaye\nfigue\nananas\n")
    with open(fichier, 'r') as f:
        return [ligne.strip() for ligne in f.readlines()]

def ajouter_mot(fichier, mot):
    # Ajoute un mot dans le fichier.#
    with open(fichier, 'a') as f:
        f.write(mot + "\n")

def choisir_mot(mots):
    # Choisit un mot au hasard dans la liste.#
    return random.choice(mots)

def afficher_mot(mot, lettres_trouvees):
    # Affiche le mot avec des '_' pour les lettres non trouvées. #
    return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot])

def jeu_pendu():
    pygame.init()

    # Paramètres
    largeur, hauteur = 800, 600
    fond_couleur = (255, 255, 255)
    texte_couleur = (0, 0, 0)
    police_taille = 48
    fichier_mots = "mots.txt"
    images_pendu = [f"etape_{i}.png" for i in range(7)]

    # Charger la police personnalisée
    police_personnalisee = pygame.font.Font("PlaywriteVN-VariableFont_wght.ttf", police_taille)

    # Initialisation
    ecran = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Jeu du Pendu")

    mots = lire_mots(fichier_mots)

    def afficher_texte(texte, x, y):
        # Affiche un texte sur l'écran avec la police personnalisée. #
        rendu = police_personnalisee.render(texte, True, texte_couleur)
        ecran.blit(rendu, (x, y))

    def afficher_texte_multiligne(texte, x, y, largeur_max, espacement=10):
        # Affiche un texte en plusieurs lignes si nécessaire.#
        lignes = []
        mots = texte.split(' ')
        ligne_actuelle = ""

        for mot in mots:
            test_ligne = f"{ligne_actuelle} {mot}".strip()
            if police_personnalisee.size(test_ligne)[0] <= largeur_max:
                ligne_actuelle = test_ligne
            else:
                lignes.append(ligne_actuelle)
                ligne_actuelle = mot

        if ligne_actuelle:
            lignes.append(ligne_actuelle)

        for i, ligne in enumerate(lignes):
            rendu = police_personnalisee.render(ligne, True, texte_couleur)
            ecran.blit(rendu, (x, y + i * (police_taille + espacement)))

    def jouer():
        mot = choisir_mot(mots)
        lettres_trouvees = set()
        lettres_ratees = set()
        erreurs = 0
        jeu_termine = False

        while not jeu_termine:
            ecran.fill(fond_couleur)

            # Affichage du pendu
            image_pendu = pygame.image.load(images_pendu[erreurs])
            ecran.blit(image_pendu, (50, 50))

            # Affichage du mot
            mot_affiche = afficher_mot(mot, lettres_trouvees)
            afficher_texte(mot_affiche, 200, 400)

            # Affichage des lettres ratées
            afficher_texte("Ratées : " + ' '.join(sorted(lettres_ratees)), 200, 500)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quitter"

                if event.type == pygame.KEYDOWN:
                    lettre = event.unicode.lower()
                    if lettre.isalpha() and lettre not in lettres_trouvees | lettres_ratees:
                        if lettre in mot:
                            lettres_trouvees.add(lettre)
                        else:
                            lettres_ratees.add(lettre)
                            erreurs += 1

                        if erreurs == len(images_pendu) - 1:
                            jeu_termine = True

                        if set(mot) <= lettres_trouvees:
                            jeu_termine = True

        # Résultat
        ecran.fill(fond_couleur)
        if erreurs == len(images_pendu) - 1:
            message = f"Perdu ! Le mot était : {mot}"
        else:
            message = "Félicitations ! Vous avez gagné !"

        afficher_texte_multiligne(message, 100, 250, largeur_max=600, espacement=10)
        pygame.display.flip()
        pygame.time.wait(3000)

    def menu():
        while True:
            ecran.fill(fond_couleur)
            afficher_texte("1. Jouer", 200, 200)
            afficher_texte("2. Ajouter un mot", 200, 300)
            afficher_texte("3. Quitter", 200, 400)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        result = jouer()
                        if result == "quitter":
                            return
                    elif event.key == pygame.K_2:
                        ajouter_un_mot()
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        return

    def ajouter_un_mot():
        mot = ""
        while True:
            ecran.fill(fond_couleur)
            afficher_texte("Entrez un mot (appuyez sur Entrée pour valider):", 50, 200)
            afficher_texte(mot, 50, 300)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and mot:
                        ajouter_mot(fichier_mots, mot)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        mot = mot[:-1]
                    elif event.unicode.isalpha():
                        mot += event.unicode.lower()

    menu()

if __name__ == "__main__":
    jeu_pendu()


# # Version en Français #
# import pygame
# import random
# import os

# def lire_mots(fichier):
#     # Lit les mots du fichier et retourne une liste.#
#     if not os.path.exists(fichier):
#         with open(fichier, 'w') as f:
#             f.write("pomme\nbanane\ncerise\norange\nmangue\nraisin\npoire\nfraise\nprune\nkiwi\ncitron\ngoyave\npapaye\nfigue\nananas\n")
#     with open(fichier, 'r') as f:
#         return [ligne.strip() for ligne in f.readlines()]

# def ajouter_mot(fichier, mot):
#     # Ajoute un mot dans le fichier.#
#     with open(fichier, 'a') as f:
#         f.write(mot + "\n")

# def choisir_mot(mots):
#     # Choisit un mot au hasard dans la liste.#
#     return random.choice(mots)

# def afficher_mot(mot, lettres_trouvees):
#     # Affiche le mot avec des '_' pour les lettres non trouvées.#
#     return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot])

# def jeu_pendu():
#     pygame.init()

#     # Paramètres
#     largeur, hauteur = 800, 600
#     fond_couleur = (255, 255, 255)
#     texte_couleur = (0, 0, 0)
#     police_taille = 48
#     fichier_mots = "mots.txt"
#     images_pendu = [f"etape_{i}.png" for i in range(7)]

#     # Charger la police personnalisée
#     police_personnalisee = pygame.font.Font("PlaywriteVN-VariableFont_wght.ttf", police_taille)

#     # Initialisation
#     ecran = pygame.display.set_mode((largeur, hauteur))
#     pygame.display.set_caption("Jeu du Pendu")

#     mots = lire_mots(fichier_mots)

#     def afficher_texte(texte, x, y):
#         # Affiche un texte sur l'écran avec la police personnalisée.#
#         rendu = police_personnalisee.render(texte, True, texte_couleur)
#         ecran.blit(rendu, (x, y))

#     def jouer():
#         mot = choisir_mot(mots)
#         lettres_trouvees = set()
#         lettres_ratees = set()
#         erreurs = 0
#         jeu_termine = False

#         while not jeu_termine:
#             ecran.fill(fond_couleur)
            
#             # Affichage du pendu
#             image_pendu = pygame.image.load(images_pendu[erreurs])
#             ecran.blit(image_pendu, (50, 50))

#             # Affichage du mot
#             mot_affiche = afficher_mot(mot, lettres_trouvees)
#             afficher_texte(mot_affiche, 200, 400)

#             # Affichage des lettres ratées
#             afficher_texte("Ratées : " + ' '.join(sorted(lettres_ratees)), 200, 500)

#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     return "quitter"

#                 if event.type == pygame.KEYDOWN:
#                     lettre = event.unicode.lower()
#                     if lettre.isalpha() and lettre not in lettres_trouvees | lettres_ratees:
#                         if lettre in mot:
#                             lettres_trouvees.add(lettre)
#                         else:
#                             lettres_ratees.add(lettre)
#                             erreurs += 1

#                         if erreurs == len(images_pendu) - 1:
#                             jeu_termine = True

#                         if set(mot) <= lettres_trouvees:
#                             jeu_termine = True

#         # Résultat
#         # ecran.fill(fond_couleur)
#         # if erreurs == len(images_pendu) - 1:
#         #     afficher_texte(f"Perdu ! Le mot était : {mot}", 200, 300)
#         # else:
#         #     afficher_texte("Félicitations ! Vous avez gagné !", 200, 300)
#         # pygame.display.flip()
#         # pygame.time.wait(3000)
#         ecran.fill(fond_couleur)
#         if erreurs == len(images_pendu) - 1:
#             message = f"Perdu ! Le mot était : {mot}"
#         else:
#             message = "Félicitations ! Vous avez gagné !"

#         # Afficher le message avec une largeur maximale de 600 pixels
#         afficher_texte_multiligne(message, 100, 250, largeur_max=600, espacement=10)

#         pygame.display.flip()
#         pygame.time.wait(3000)


#     def menu():
#         while True:
#             ecran.fill(fond_couleur)
#             afficher_texte("1. Jouer", 200, 200)
#             afficher_texte("2. Ajouter un mot", 200, 300)
#             afficher_texte("3. Quitter", 200, 400)
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_1:
#                         result = jouer()
#                         if result == "quitter":
#                             return
#                     elif event.key == pygame.K_2:
#                         ajouter_un_mot()
#                     elif event.key == pygame.K_3:
#                         pygame.quit()
#                         return

#     def ajouter_un_mot():
#         mot = ""
#         while True:
#             ecran.fill(fond_couleur)
#             afficher_texte("Entrez un mot (appuyez sur Entrée pour valider):", 50, 200)
#             afficher_texte(mot, 50, 300)
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN and mot:
#                         ajouter_mot(fichier_mots, mot)
#                         return
#                     elif event.key == pygame.K_BACKSPACE:
#                         mot = mot[:-1]
#                     elif event.unicode.isalpha():
#                         mot += event.unicode.lower()

#     menu()

# if __name__ == "__main__":
#     jeu_pendu()

# Version en Anglais #

# import pygame
# import random
# import os

# def read_words(file):
#     # Reads words from the file and returns a list.#
#     if not os.path.exists(file):
#         with open(file, 'w') as f:
#             f.write("apple\nbanana\ncherry\norange\nmango\ngrape\npear\nstrawberry\nplum\nkiwi\nlemon\nguava\npapaya\nfig\npineapple\n")
#     with open(file, 'r') as f:
#         return [line.strip() for line in f.readlines()]

# def add_word(file, word):
#     # Adds a word to the file.#
#     with open(file, 'a') as f:
#         f.write(word + "\n")

# def choose_word(words):
#     # Randomly chooses a word from the list.#
#     return random.choice(words)

# def display_word(word, guessed_letters):
#     # Displays the word with '_' for unguessed letters.#
#     return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# def hangman_game():
#     pygame.init()

#     # Settings
#     width, height = 800, 600
#     background_color = (255, 255, 255)
#     text_color = (0, 0, 0)
#     font_size = 48
#     words_file = "words.txt"
#     hangman_images = [f"step_{i}.png" for i in range(7)]

#     # Load custom font
#     custom_font = pygame.font.Font("PlaywriteVN-VariableFont_wght.ttf", font_size)

#     # Initialization
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("Hangman Game")

#     words = read_words(words_file)

#     def display_text(text, x, y):
#         # Displays text on the screen with the custom font.#
#         rendered = custom_font.render(text, True, text_color)
#         screen.blit(rendered, (x, y))

#     def play():
#         word = choose_word(words)
#         guessed_letters = set()
#         missed_letters = set()
#         mistakes = 0
#         game_over = False

#         while not game_over:
#             screen.fill(background_color)
            
#             # Display hangman
#             hangman_image = pygame.image.load(hangman_images[mistakes])
#             screen.blit(hangman_image, (50, 50))

#             # Display the word
#             displayed_word = display_word(word, guessed_letters)
#             display_text(displayed_word, 200, 400)

#             # Display missed letters
#             display_text("Missed: " + ' '.join(sorted(missed_letters)), 200, 500)

#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     return "quit"

#                 if event.type == pygame.KEYDOWN:
#                     letter = event.unicode.lower()
#                     if letter.isalpha() and letter not in guessed_letters | missed_letters:
#                         if letter in word:
#                             guessed_letters.add(letter)
#                         else:
#                             missed_letters.add(letter)
#                             mistakes += 1

#                         if mistakes == len(hangman_images) - 1:
#                             game_over = True

#                         if set(word) <= guessed_letters:
#                             game_over = True

#         # Result
#         screen.fill(background_color)
#         if mistakes == len(hangman_images) - 1:
#             display_text(f"You lost! The word was: {word}", 200, 300)
#         else:
#             display_text("Congratulations! You won!", 200, 300)
#         pygame.display.flip()
#         pygame.time.wait(3000)

#     def menu():
#         while True:
#             screen.fill(background_color)
#             display_text("1. Play", 200, 200)
#             display_text("2. Add a word", 200, 300)
#             display_text("3. Quit", 200, 400)
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_1:
#                         result = play()
#                         if result == "quit":
#                             return
#                     elif event.key == pygame.K_2:
#                         add_a_word()
#                     elif event.key == pygame.K_3:
#                         pygame.quit()
#                         return

#     def add_a_word():
#         word = ""
#         while True:
#             screen.fill(background_color)
#             display_text("Enter a word (press Enter to confirm):", 50, 200)
#             display_text(word, 50, 300)
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN and word:
#                         add_word(words_file, word)
#                         return
#                     elif event.key == pygame.K_BACKSPACE:
#                         word = word[:-1]
#                     elif event.unicode.isalpha():
#                         word += event.unicode.lower()

#     menu()

# if __name__ == "__main__":
#     hangman_game()
