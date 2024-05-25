import pygame
from sys import exit
from random import randint, choice
import math

from player import Player

from obstacles import Obstacles

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Crossy Sky')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/NicoClean-Regular.otf', 40)
title_font = pygame.font.Font('font/NicoClean-Regular.otf', 60)
arrows_font = pygame.font.Font('font/NicoPups-Regular.otf', 40)
game_active = False
start_time = 0
score = 0
start_score = 0
difficulty_level = 0
START_DIFFICULTY = 1300
MAX_DIFFICULTY = 250
birds = ['White', 'Blue', 'Cardinal', 'Robin', 'Sparrow']
birds_index = 0
bird_choose = True

sky_backgrounds = ['Sunny Sky', 'Rainy Sky', 'Stormy Sky']
sky_background_index = 0
sky_surface = pygame.image.load(f'graphics/background/{sky_backgrounds[sky_background_index]}.png').convert_alpha()
sky_surface = pygame.transform.rotozoom(sky_surface, 0, 0.4)

obstacle_group = pygame.sprite.Group()


def display_score():
    score_surf = test_font.render(f'Score: {score}', False, (225, 245, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)


def level_up(score, difficulty):
    if player.sprite.rect.bottom < 0:
        player.sprite.rect.top = 780
        score += 1
        if START_DIFFICULTY - difficulty > MAX_DIFFICULTY:
            difficulty += 150
        pygame.time.set_timer(obstacle_timer, int(START_DIFFICULTY - difficulty))
    return score, difficulty


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        pygame.time.set_timer(obstacle_timer, START_DIFFICULTY)
        return False
    else:
        return True

# Intro screen
# def intro_screen(birds, birds_index):
#     player_stand = pygame.image.load(f'graphics/Birds/{birds[birds_index]}/tile001.png').convert_alpha()
#     player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
#     player_stand_rect = player_stand.get_rect(center=(400, 400))
#     return player_stand, player_stand_rect

# intro_screen(birds, birds_index)
game_name = title_font.render('Crossy Sky', False, (225, 245, 255))
game_name_rect = game_name.get_rect(center=(400, 280))

game_message = arrows_font.render('Press UP to fly', False, (225, 245, 255))
game_message_rect = game_message.get_rect(center=(400, 540))

right_arrow = arrows_font.render('>', False, (225, 245, 255))
right_arrow_rect = right_arrow.get_rect(center=(500,400))

left_arrow = arrows_font.render('<', False, (225, 245, 255))
left_arrow_rect = right_arrow.get_rect(center=(300, 400))

# Clouds - Difficulty levels:
sunny_cloud = pygame.image.load('graphics/Regular Cloud.png').convert_alpha()
sunny_cloud = pygame.transform.rotozoom(sunny_cloud, 0, 0.25)
sunny_cloud_rect = sunny_cloud.get_rect(center=(160,150))
rainy_cloud = pygame.image.load('graphics/Rain Cloud.png').convert_alpha()
rainy_cloud = pygame.transform.rotozoom(rainy_cloud, 0, 0.25)
rainy_cloud_rect = rainy_cloud.get_rect(center=(410,160))
stormy_cloud = pygame.image.load('graphics/Storm Cloud.png').convert_alpha()
stormy_cloud = pygame.transform.rotozoom(stormy_cloud, 0, 0.25)
stormy_cloud_rect = stormy_cloud.get_rect(center=(650, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, START_DIFFICULTY)

# The Game Loop:
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['eagle'])))

        else:
            if bird_choose:
                player = pygame.sprite.GroupSingle()
                player.add(Player(birds[birds_index]))
                bird_choose = False
            if player.sprite.rect.colliderect(rainy_cloud_rect):
                game_active = True
                score = 0
                difficulty_level = 0
                player.sprite.rect.bottom = 780
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if birds_index == len(birds) - 1:
                        birds_index = 0
                    else:
                        birds_index += 1
                if event.key == pygame.K_LEFT:
                    if birds_index == 0:
                        birds_index = len(birds) - 1
                    else:
                        birds_index -= 1
            # intro_screen(birds, birds_index)



    if game_active:
        screen.blit(sky_surface, (0, 0))
        display_score()

        player.draw(screen)
        player.update()
        score, difficulty_level = level_up(score, difficulty_level)


        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        if not game_active: bird_choose = True


    else:
        screen.fill((44, 141, 222))

        score_message = arrows_font.render(f'Your score: {score}', False, (225, 245, 255))
        score_message_rect = score_message.get_rect(center=(400, 330))

        screen.blit(sunny_cloud, sunny_cloud_rect)
        screen.blit(rainy_cloud, rainy_cloud_rect)
        screen.blit(stormy_cloud, stormy_cloud_rect)
        screen.blit(game_name, game_name_rect)

        obstacle_group.empty()

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

        player.draw(screen)
        player.update()

    pygame.display.update()
    clock.tick(60)
