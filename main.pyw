import pygame
import classes
import others
import game

def main():
    pygame.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])

    # ablak
    pygame.display.set_caption("A Gyurcsány Show: A videójáték | Nemzeti Videójáték Stúdió")
    pygame.display.set_icon(pygame.image.load("Files/icon.png").convert())
    window = pygame.display.set_mode(classes.Screen.resolution, flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL, vsync = 1)

    classes.CharacterData.load()

    try:
        classes.Settings.load()
    except:
        classes.Screen.fps_index = 0
        classes.Settings.music = True
        for i in classes.CharacterData.characters:
            i.score = 0
        classes.CharacterData.last_choice = 0

    # zene
    pygame.mixer.music.load("Files/bg_music.mp3")
    pygame.mixer.music.queue("Files/bg_music.mp3")
    if classes.Settings.music:
        pygame.mixer.music.set_volume(1.0)
    else:
        pygame.mixer.music.set_volume(0.0)
    pygame.mixer.music.play(-1)

    # képernyőn megjelenő elemek
    background = classes.Items(pygame.image.load("Files/bg.jpg").convert(), (0, 0), False)
    bg_patch = classes.Items(pygame.image.load("Files/patch.jpg").convert(), (470, 475), False)
    play_button = classes.Items(pygame.image.load("Files/game_button.png").convert_alpha(), (640, 540), True)
    loud = classes.Items(pygame.image.load("Files/loud.png").convert_alpha(), (1207, 647), False)
    mute = classes.Items(pygame.image.load("Files/mute.png").convert_alpha(), (1207, 647), False)
    mini_field = classes.Items(pygame.image.load("Files/mini_field.png").convert_alpha(), (1073, 647), False)
    mistral_40 = pygame.font.Font("Files/mistral.ttf", 40)

    act_button_size = [ play_button.texture.get_width(), play_button.texture.get_height() ]
    pulse = True
    clicked = False

    window.blit(background.texture, background.pos)

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                classes.Settings.save()
                run = False
            elif others.button_click(play_button, event):
                clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
                clicked = False
                classes.CharacterData.last_choice = game.choose_character(window)
                game_result = game.game(window)
                game.results(window, False, game_result, classes.CharacterData.last_choice)
                window.blit(background.texture, background.pos)
            elif others.button_click(mute, event):
                if classes.Settings.music:
                    classes.Settings.music = False
                    pygame.mixer.music.set_volume(0.0)
                else:
                    classes.Settings.music = True
                    pygame.mixer.music.set_volume(1.0)
            elif others.button_click(mini_field, event):
                classes.Screen.fps_step()

        window.blit(bg_patch.texture, bg_patch.pos)
        pulse = others.button_pulse(pulse, play_button, act_button_size, window, (classes.Screen.resolution[0] // 2, 3 * classes.Screen.resolution[1] // 4))
        if classes.Settings.music:
            window.blit(mute.texture, mute.pos)
        else:
            window.blit(loud.texture, loud.pos)
        window.blit(mini_field.texture, mini_field.pos)
        fps_text = classes.Items(mistral_40.render(f"FPS: {classes.Screen.fps_options[classes.Screen.fps_index]}", True, classes.Screen.purple), (1137, 681), True)
        window.blit(fps_text.texture, fps_text.pos)

        clock.tick(60) # ez fix
        pygame.display.update()

    pygame.quit()

main()