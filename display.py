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
pygame.time.delay(4500)

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

        pygame.display.flip()
    pygame.quit()

draw_hangman()
def load_animation_frames(path, file_format="png"):
    frames = []
    for frame_file in sorted(os.listdir(path), key=lambda x: int(x.split('_')[-1].split('.')[0])):
        if frame_file.endswith(file_format):
            frame_path = os.path.join(path, frame_file)
            frames.append(pygame.image.load(frame_path).convert_alpha())
    return frames



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
    