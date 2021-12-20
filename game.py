import pygame
import classes
import math
import others
import sys
import random
from others import ShapeTypes

def game(window = pygame.display.set_mode(classes.Screen.resolution, flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL, vsync = 1)):
    background = classes.Items(pygame.image.load("Files/bg.jpg").convert(), (0, 0), False)
    field_bg = classes.Items(pygame.image.load("Files/bg_game.png").convert_alpha(), (31, 66), False)
    field_bg_mini = classes.Items(pygame.image.load("Files/bg_game_mini.png").convert_alpha(), (1155, 360), True)
    sum_icon = classes.Items(pygame.image.load("Files/sum.png").convert_alpha(), (1155, 335), True)
    steps_icon = classes.Items(pygame.image.load("Files/steps.png").convert_alpha(), (1155, 460), True)
    border = classes.Items(pygame.image.load("Files/border.png").convert_alpha())
    selected = classes.Items(pygame.image.load("Files/selected.png").convert_alpha())
    loud = classes.Items(pygame.image.load("Files/loud.png").convert_alpha(), (1207, 647), False)
    mute = classes.Items(pygame.image.load("Files/mute.png").convert_alpha(), (1207, 647), False)
    mini_field = classes.Items(pygame.image.load("Files/mini_field.png").convert_alpha(), (1073, 647), False)
    mistral_40 = pygame.font.Font("Files/mistral.ttf", 40)
    corner = (47, 75)
    field_size = (10, 17)

    drag = False
    clicked = False
    clicked_pos = ()
    startpos = ()
    moving_elements = []
    change = True
    field_change = False
    to_collect = random.randint(25, 50)
    max_steps = random.randint(int(to_collect * 1.05), int(to_collect * 1.25))
    nums = classes.Numbers(e_num=to_collect, steps=max_steps)
    etalon = others.random_party()((1155, 210), True)
    check = True
    initial = True
    gameover = False

    field = []
    for _ in range(field_size[0]):
        field.append([others.random_party()((0, 0), False) for _ in range(field_size[1])])

    clock = pygame.time.Clock()
    run = True
    while run:
        if nums.steps <= 0 or nums.etalon_num <= 0:
            gameover = True

        if check and classes.Moving.active_field_swap == 0: # az automatikus leszedés előnyt élvez a felhasználóval szemben
            check = False
            match = True
            while match:
                match = False
                i = 0
                while i < len(field) and not match:
                    j = 0
                    while j < len(field[i]) and not match:
                        actual = others.shape_analysis(field, others.collect_same(field, (i, j), (i, j), []))
                        if not actual[0] == None:
                            match = True
                            check = True
                            if actual[0] == ShapeTypes.THREE_IN_ROW:
                                others.remove_tiles(field, actual, None, etalon, sum_icon, nums, moving_elements)
                            elif actual[0] in ShapeTypes.GadgetDict:
                                others.remove_tiles(field, actual, None, etalon, sum_icon, nums, moving_elements)
                                field[i][j] = ShapeTypes.GadgetDict[actual[0]]((corner[0] + j * border.texture.get_width() + 3, corner[1] + i * border.texture.get_height() + 3), False)

                        j += 1
                    
                    i += 1
            others.arrange_field(field, field_size, moving_elements, corner, border)

            if not check and not others.can_move(field): # nincs lehetséges lépés, újrakeverünk
                check = True
                others.reshuffle(field, field_size, corner, border, moving_elements)
            if initial:
                moving_elements = [ ]
                classes.Moving.active_field_swap = 0
                nums.all_num = 0
                nums.etalon_num = to_collect
                nums.steps = max_steps
                if not check:
                    initial = False
                    for i in range(len(field)):
                        for j in range(len(field[i])):
                            field[i][j].new_pos((corner[0] + j * border.texture.get_width() + 3, 0 - (field_size[0] - i) * (border.texture.get_height()) * 2 + 3), False)
                            moving_elements.append(classes.Moving(field[i][j], (corner[0] + j * border.texture.get_width() + 3, corner[1] + i * border.texture.get_height() + 3), True))

        for event in pygame.event.get(): # felhasználói interakció
            if event.type == pygame.QUIT:
                classes.Settings.save()
                sys.exit()
            elif others.button_click(mute, event):
                if classes.Settings.music:
                    classes.Settings.music = False
                    pygame.mixer.music.set_volume(0.0)
                else:
                    classes.Settings.music = True
                    pygame.mixer.music.set_volume(1.0)
                change = True
            elif others.button_click(mini_field, event):
                classes.Screen.fps_step()
                change = True
            elif not gameover:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # húzás kezdése
                    if classes.Moving.active_field_swap == 0:
                        drag = True
                        startpos = event.pos
                        cord = others.get_field_cord(corner, event.pos, border, field_size)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drag: # ha a húzás nem elég hozzú, akkor kattintás
                    drag = False
                    if not clicked and classes.Moving.active_field_swap == 0:
                        cord = others.get_field_cord(corner, event.pos, border, field_size)
                        if not cord == None:
                            clicked_pos = cord
                            clicked = True
                            change = True
                    elif clicked:
                        cord = others.get_field_cord(corner, event.pos, border, field_size)
                        if cord == None:
                            pass
                        elif cord == clicked_pos:
                            if isinstance(field[cord[0]][cord[1]], classes.Gadgets):
                                field[cord[0]][cord[1]].activate(field, cord, etalon, sum_icon, moving_elements, nums)
                                nums.steps -= 1
                                others.arrange_field(field, field_size, moving_elements, corner, border)
                                check = True
                        elif abs(cord[0] - clicked_pos[0]) <= 1 ^ abs(cord[1] - clicked_pos[1]) <= 1: # XOR operátor: csak az egyik lehet igaz
                            other_one = clicked_pos
                            others.swap_tiles(field, field_size, cord, other_one, moving_elements)
                            field_change = True
                        clicked = False
                        change = True
                elif event.type == pygame.MOUSEMOTION and drag: # húzás
                    if math.sqrt((event.pos[0] - startpos[0]) ** 2 + (event.pos[1] - startpos[1]) ** 2) > 25: # 25px táv után
                        drag = False
                        try: # kell, mert ha mezőn kívül húz egyet a felhasználó, kivétel keletkezik
                            drag_cord = others.drag_direction((event.pos[0] - startpos[0], event.pos[1] - startpos[1]))
                            other_one = (cord[0] + drag_cord[0], cord[1] + drag_cord[1])
                            others.swap_tiles(field, field_size, cord, other_one, moving_elements)
                            change = True
                            field_change = True
                            clicked = False
                        except:
                            pass

        if field_change:
            cord1 = cord # ide zároljuk magunknak őket, nehogy véletlenül felülírja valami, amíg várunk lejjebb
            cord2 = other_one
            if classes.Moving.active_field_swap == 0:
                side_one = others.shape_analysis(field, others.collect_same(field, cord1, cord1, []))
                side_two = others.shape_analysis(field, others.collect_same(field, cord2, cord2, []))
                if ((side_one[0] == None and side_two[0] == None) or type(field[cord1[0]][cord1[1]]) == type(field[cord2[0]][cord2[1]])) and not (isinstance(field[cord1[0]][cord1[1]], classes.Gadgets) or isinstance(field[cord2[0]][cord2[1]], classes.Gadgets)):
                    others.swap_tiles(field, field_size, cord1, cord2, moving_elements)
                    check = False
                else:
                    if isinstance(field[cord1[0]][cord1[1]], classes.Gadgets):
                        field[cord1[0]][cord1[1]].activate(field, cord1, etalon, sum_icon, moving_elements, nums)
                    if isinstance(field[cord2[0]][cord2[1]], classes.Gadgets):
                        field[cord2[0]][cord2[1]].activate(field, cord2, etalon, sum_icon, moving_elements, nums)
                    if side_one[0] == ShapeTypes.THREE_IN_ROW or side_two[0] == ShapeTypes.THREE_IN_ROW:
                        others.remove_tiles(field, side_one, side_two, etalon, sum_icon, nums, moving_elements)
                    if side_one[0] in ShapeTypes.GadgetDict or side_two[0] in ShapeTypes.GadgetDict:
                        others.remove_tiles(field, side_one, side_two, etalon, sum_icon, nums, moving_elements)
                        if side_one[0] in ShapeTypes.GadgetDict:
                            field[cord1[0]][cord1[1]] = ShapeTypes.GadgetDict[side_one[0]]((corner[0] + cord1[1] * border.texture.get_width() + 3, corner[1] + cord1[0] * border.texture.get_height() + 3), False)
                        if side_two[0] in ShapeTypes.GadgetDict:
                            field[cord2[0]][cord2[1]] = ShapeTypes.GadgetDict[side_two[0]]((corner[0] + cord2[1] * border.texture.get_width() + 3, corner[1] + cord2[0] * border.texture.get_height() + 3), False)

                    nums.steps -= 1
                    others.arrange_field(field, field_size, moving_elements, corner, border)
                    check = True
                field_change = False

        if not initial:
            if len(moving_elements) > 0 or change:
                window.blit(background.texture, background.pos)
                window.blit(field_bg.texture, field_bg.pos)
                window.blit(field_bg_mini.texture, field_bg_mini.pos)

                window.blit(etalon.texture, etalon.pos)
                if nums.etalon_num >= 0:
                    etalon_text = classes.Items(mistral_40.render(str(nums.etalon_num), True, classes.Screen.blue), (1155, 270), True)
                else:
                    etalon_text = classes.Items(mistral_40.render("0", True, classes.Screen.blue), (1155, 270), True)
                window.blit(etalon_text.texture, etalon_text.pos)
                window.blit(sum_icon.texture, sum_icon.pos)
                sum_text = classes.Items(mistral_40.render(str(nums.all_num), True, classes.Screen.blue), (1155, 395), True)
                window.blit(sum_text.texture, sum_text.pos)
                window.blit(steps_icon.texture, steps_icon.pos)
                steps_text = classes.Items(mistral_40.render(str(nums.steps), True, classes.Screen.blue), (1155, 520), True)
                window.blit(steps_text.texture, steps_text.pos)

                if classes.Settings.music:
                    window.blit(mute.texture, mute.pos)
                else:
                    window.blit(loud.texture, loud.pos)
                window.blit(mini_field.texture, mini_field.pos)
                fps_text = classes.Items(mistral_40.render(f"FPS: {classes.Screen.fps_options[classes.Screen.fps_index]}", True, classes.Screen.purple), (1137, 681), True)
                window.blit(fps_text.texture, fps_text.pos)

                for i in range(field_size[0]):
                    for j in range(field_size[1]):
                        window.blit(border.texture, (corner[0] + j * border.texture.get_width(), corner[1] + i * border.texture.get_height()))
                        if not field[i][j] == None and not field[i][j].moving:
                            if clicked and (i, j) == clicked_pos:
                                window.blit(selected.texture, (corner[0] + j * border.texture.get_width(), corner[1] + i * border.texture.get_height()))
                            window.blit(field[i][j].texture, field[i][j].pos)
                
                length = len(moving_elements)
                others.element_mover(moving_elements, window)
                if len(moving_elements) == 0 and not len(moving_elements) == length:
                    change = True # az utolsó képkockát még ki kell adnia, ha most váltott 0-ra a lista hossza
                else:
                    change = False

            if gameover and len(moving_elements) == 0 and not change:
                run = False

            pygame.display.update()
        clock.tick(classes.Screen.fps_options[classes.Screen.fps_index])
    if nums.etalon_num <= 0:
        return (True, nums.all_num)
    else:
        return (False, nums.all_num)

def choose_character(window):
    background = classes.Items(pygame.image.load("Files/bg.jpg").convert(), (0, 0), False)
    bg_faces = classes.Items(pygame.image.load("Files/bg_faces.png").convert_alpha(), (640, 360), True)
    bg_patch = classes.Items(pygame.image.load("Files/bg_face_patch.png").convert_alpha(), (640, 360), True)
    loud = classes.Items(pygame.image.load("Files/loud.png").convert_alpha(), (1207, 647), False)
    mute = classes.Items(pygame.image.load("Files/mute.png").convert_alpha(), (1207, 647), False)
    mini_field = classes.Items(pygame.image.load("Files/mini_field.png").convert_alpha(), (1073, 647), False)
    left = classes.Items(pygame.image.load("Files/left.png").convert_alpha(), (475, 360), True)
    right = classes.Items(pygame.image.load("Files/right.png").convert_alpha(), (805, 360), True)
    go = classes.Items(pygame.image.load("Files/go.png").convert_alpha(), (640, 620))
    left_end = classes.Items(pygame.image.load("Files/left_end.png").convert_alpha())
    right_end = classes.Items(pygame.image.load("Files/right_end.png").convert_alpha())
    center = classes.Items(pygame.image.load("Files/center.png").convert_alpha())
    mistral_40 = pygame.font.Font("Files/mistral.ttf", 40)
    mistral_50 = pygame.font.Font("Files/mistral.ttf", 50)

    act_button_size = [ go.texture.get_width(), go.texture.get_height() ]
    pulse = True

    moving_elements = [ ]

    clock = pygame.time.Clock()
    run = True
    while run:
        current_face = classes.Items(classes.CharacterData.characters[classes.CharacterData.last_choice].pic, (640, 360), True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                classes.Settings.save()
                sys.exit()
            elif others.button_click(mute, event):
                if classes.Settings.music:
                    classes.Settings.music = False
                    pygame.mixer.music.set_volume(0.0)
                else:
                    classes.Settings.music = True
                    pygame.mixer.music.set_volume(1.0)
            elif others.button_click(mini_field, event):
                classes.Screen.fps_step()
            elif others.button_click(left, event) and len(moving_elements) == 0:
                classes.CharacterData.last_choice = (classes.CharacterData.last_choice + 1) % len(classes.CharacterData.characters)
                moving_elements.append(classes.Moving(current_face, (303, 260)))
                current_face = classes.Items(classes.CharacterData.characters[classes.CharacterData.last_choice].pic, (803, 260), False)
                moving_elements.append(classes.Moving(current_face, (553, 260)))
            elif others.button_click(right, event) and len(moving_elements) == 0:
                if classes.CharacterData.last_choice == 0:
                    classes.CharacterData.last_choice = len(classes.CharacterData.characters) - 1
                else:
                    classes.CharacterData.last_choice -= 1
                moving_elements.append(classes.Moving(current_face, (803, 260)))
                current_face = classes.Items(classes.CharacterData.characters[classes.CharacterData.last_choice].pic, (303, 260), False)
                moving_elements.append(classes.Moving(current_face, (553, 260)))
            elif others.button_click(go, event):
                return classes.CharacterData.last_choice
        
        window.blit(background.texture, background.pos)
        if classes.Settings.music:
            window.blit(mute.texture, mute.pos)
        else:
            window.blit(loud.texture, loud.pos)
        window.blit(mini_field.texture, mini_field.pos)
        fps_text = classes.Items(mistral_40.render(f"FPS: {classes.Screen.fps_options[classes.Screen.fps_index]}", True, classes.Screen.purple), (1137, 681), True)
        window.blit(fps_text.texture, fps_text.pos)
        window.blit(bg_faces.texture, bg_faces.pos)
        if len(moving_elements) == 0:
            window.blit(current_face.texture, current_face.pos)
        face_text = classes.Items(mistral_50.render(classes.CharacterData.characters[classes.CharacterData.last_choice].name, True, classes.Screen.blue), (640, 525), True)
        pieces = face_text.texture.get_width() // 35
        start = round(640 - (pieces / 2 + 1) * 35)
        window.blit(left_end.texture, (start, 490))
        start += 35
        for i in range(pieces):
            window.blit(center.texture, (start, 490))
            start += 35
        window.blit(right_end.texture, (start, 490))
        window.blit(face_text.texture, face_text.pos)
        others.element_mover(moving_elements, window)
        window.blit(bg_patch.texture, bg_patch.pos)
        window.blit(left.texture, left.pos)
        window.blit(right.texture, right.pos)
        pulse = others.button_pulse(pulse, go, act_button_size, window, (640, 620))

        clock.tick(60) # pulse miatt fix
        pygame.display.update()

def results(window, only_see, result = None, character = None):
    if only_see:
        data = sorted(classes.CharacterData.characters, key=classes.Characters.sort_key, reverse=True)
    else:
        if result[0]:
            print("Gratulálok, sikeresen meghosszabbítottad a Gyurcsány-showt egy újabb évaddal!")
            classes.CharacterData.characters[character].score += result[1]
        else:
            print("Ez a bukott műsor nem kapott újabb esélyt.")
        data = sorted(classes.CharacterData.characters, key=classes.Characters.sort_key, reverse=True)

    for i in range(len(data)):
        print(f"{i + 1}.: {data[i].name}, {data[i].score} pont.")
    
    input("Nyomd meg az entert a továbblépéshez!")