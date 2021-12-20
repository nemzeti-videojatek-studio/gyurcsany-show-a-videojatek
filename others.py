import pygame
import classes
import random
from classes import ShapeTypes

def button_pulse(pulse, button, size, window, pos):
    if size[0] > button.texture.get_width() * 1.05:
        pulse = False
    elif size[0] < button.texture.get_width() * 0.95:
        pulse = True

    if pulse:
        size[0] += 1
        size[1] += 1
    else:
        size[0] -= 1
        size[1] -= 1

    modified = classes.Items(pygame.transform.scale(button.texture, tuple(size)).convert_alpha(), pos)
    window.blit(modified.texture, modified.pos)
    return pulse

def button_click(which, event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and which.texture.get_rect().collidepoint((event.pos[0] - which.pos[0], event.pos[1] - which.pos[1]))

def random_party():
    parties_list = [ classes.Fidesz, classes.Jobbik, classes.LMP, classes.Momentum, classes.MSZP, classes.Parbeszed, classes.DK, classes.MiHazank ]
    return parties_list[random.randint(0, len(parties_list) - 1)] # fontos! osztályra mutató referenciát ad, a konstruktor paramétereit ugyanúgy meg kell adni helyben: random_party()(/konktruktor paraméterek/)

def drag_direction(vector):
    if abs(vector[0]) > abs(vector[1]): # vízszintes irány lesz
        if vector[0] < 0: # balra
            return (0, -1)
        else: # jobbra
            return (0, 1)
    else:
        if vector[1] < 0: # fel
            return (-1, 0)
        else: # le
            return (1, 0)

def element_mover(to_move, window):
    if len(to_move) == 0:
        return
    move_by = 720 // classes.Screen.fps_options[classes.Screen.fps_index] # 60 fps mellett 10px/frame
    i = 0
    popped = False
    while i < len(to_move):
        if to_move[i].which == None:
            to_move.pop(i)
            popped = True
        elif to_move[i].by_x: # x tengely mentén haladunk, ott hosszabb az út, kevésbé lesz "darabos" az animáció
            if abs(to_move[i].which.pos[0] - to_move[i].where[0]) <= move_by: # ha elég közel van, a helyére mehet
                to_move[i].which.new_pos(to_move[i].where, False)
            elif to_move[i].where[0] - to_move[i].which.pos[0] < 0: # balra kell menni
                to_move[i].which.new_pos((to_move[i].which.pos[0] - move_by, (to_move[i].vector[0] * to_move[i].where[0] + to_move[i].vector[1] * to_move[i].where[1] - to_move[i].vector[0] * to_move[i].which.pos[0]) // to_move[i].vector[1]), False) # gyerekek, ezért kell megtanulni az egyenes egyenletét :)
            else: # jobbra
                to_move[i].which.new_pos((to_move[i].which.pos[0] + move_by, (to_move[i].vector[0] * to_move[i].where[0] + to_move[i].vector[1] * to_move[i].where[1] - to_move[i].vector[0] * to_move[i].which.pos[0]) // to_move[i].vector[1]), False)
        else: # y tengely szerinti mozgatás
            if abs(to_move[i].which.pos[1] - to_move[i].where[1]) <= move_by:
                to_move[i].which.new_pos(to_move[i].where, False)
            elif to_move[i].where[1] - to_move[i].which.pos[1] < 0: # fel
                to_move[i].which.new_pos(((to_move[i].vector[1] * to_move[i].where[1] + to_move[i].vector[0] * to_move[i].where[0] - to_move[i].vector[1] * to_move[i].which.pos[1]) // to_move[i].vector[0], to_move[i].which.pos[1] - move_by), False)
            else: # le
                to_move[i].which.new_pos(((to_move[i].vector[1] * to_move[i].where[1] + to_move[i].vector[0] * to_move[i].where[0] - to_move[i].vector[1] * to_move[i].which.pos[1]) // to_move[i].vector[0], to_move[i].which.pos[1] + move_by), False)

        if not popped:
            window.blit(to_move[i].which.texture, to_move[i].which.pos)

            if to_move[i].which.pos == to_move[i].where: # célba ért elemek kivétele a listáról
                to_move[i].which.moving = False
                if to_move[i].field:
                    classes.Moving.active_field_swap -= 1
                to_move.pop(i) # ez fontos, ha del-t használnék, azzal megsemmisülne a táblaelem is, a maradék szemetet a garbage collector megoldja
                i -=1

            i += 1
        else:
            popped = False

def get_field_cord(corner, pos, piece, size):
    x = (pos[0] - corner[0]) // piece.texture.get_width()
    y = (pos[1] - corner[1]) // piece.texture.get_height()
    if x < 0 or x >= size[1] or y < 0 or y >= size[0]:
        return None
    else:
        return (y, x) # mivel a tömböt fordítva indexeljük, mint a képernyőt

def swap_tiles(field, field_size, a, b, moving_elements):
    if not classes.Moving.active_field_swap == 0:
        raise ValueError # egyszerre legfeljebb 1 párt cserélünk meg a problémák elkerülése végett
    if b[0] < 0 or b[0] >= field_size[0] or b[1] < 0 or b[1] >= field_size[1]:
        raise ValueError # kimennénk a mezőről
    moving_elements.append(classes.Moving(field[a[0]][a[1]], field[b[0]][b[1]].pos, True))
    moving_elements.append(classes.Moving(field[b[0]][b[1]], field[a[0]][a[1]].pos, True))
    temp = field[a[0]][a[1]]
    field[a[0]][a[1]] = field[b[0]][b[1]]
    field[b[0]][b[1]] = temp

def collect_same(field, start_pos, act_pos, same):
    try:
        if isinstance(field[act_pos[0]][act_pos[1]], classes.Gadgets) or not type(field[start_pos[0]][start_pos[1]]) == type(field[act_pos[0]][act_pos[1]]) or field[act_pos[0]][act_pos[1]].marked or act_pos[0] < 0 or act_pos[1] < 0:
            return same
    except:
        return same
    
    same.append(act_pos)
    field[act_pos[0]][act_pos[1]].marked = True
    positions = ( -1, 1 )
    for i in positions:
        collect_same(field, start_pos, (act_pos[0] + i, act_pos[1]), same)
    for i in positions:
        collect_same(field, start_pos, (act_pos[0], act_pos[1] + i), same)
    
    return same

def shape_analysis(field, same_elemets): # az előzővel együtt kell és lehet használni
    if len(same_elemets) == 0:
        return (None, [])
    cords_x = [ [], [] ] # előforduló x koordináták és darabszámuk
    cords_y = [ [], [] ]
    for i in same_elemets: # fontos: tömbről van szó, az 1. koordináta megint az y
        if not i[0] in cords_y[0]:
            cords_y[0].append(i[0])
            cords_y[1].append(1)
        else:
            cords_y[1][cords_y[0].index(i[0])] += 1
        if not i[1] in cords_x[0]:
            cords_x[0].append(i[1])
            cords_x[1].append(1)
        else:
            cords_x[1][cords_x[0].index(i[1])] += 1
        
        field[i[0]][i[1]].marked = False
    
    to_remove = []

    max_x = max(cords_x[1])
    max_y = max(cords_y[1])

    size = (max(cords_y[0]) - min(cords_y[0]) + 1, max(cords_x[0]) - min(cords_x[0]) + 1)

    if max_y >= 3 and max_x >= 3: # nagy bomba, L és T alak
        needed_x = cords_x[0][cords_x[1].index(max_x)]
        y_min = len(field) # ettől csak kisebb lehet
        for i in same_elemets:
            if i[1] == needed_x and i[0] < y_min:
                y_min = i[0]
        for i in range(y_min, y_min + max_x):
            to_remove.append((i, needed_x))

        needed_y = cords_y[0][cords_y[1].index(max_y)]
        x_min = len(field[0]) # ettől csak kisebb lehet
        for i in same_elemets:
            if i[0] == needed_y and i[1] < x_min:
                x_min = i[1]
        for i in range(x_min, x_min + max_y):
            to_remove.append((needed_y, i))
        return (ShapeTypes.BIG_BOMB, to_remove)
    elif max_y >= 5 or max_x >= 5: # nagy bomba, egy vonal
        if max_x >= 5:
            needed_x = cords_x[0][cords_x[1].index(max_x)]
            y_min = len(field)
            for i in same_elemets:
                if i[1] == needed_x and i[0] < y_min:
                    y_min = i[0]
            for i in range(y_min, y_min + max_x):
                to_remove.append((i, needed_x))
        else:
            needed_y = cords_y[0][cords_y[1].index(max_y)]
            x_min = len(field[0])
            for i in same_elemets:
                if i[0] == needed_y and i[1] < x_min:
                    x_min = i[1]
            for i in range(x_min, x_min + max_y):
                to_remove.append((needed_y, i))
        return (ShapeTypes.BIG_BOMB, to_remove)
    elif (len(same_elemets) == 4 and size == (2, 2)) or (len(same_elemets) == 5 and ((size == (2, 3) and type(field[min(cords_y[0])][min(cords_x[0]) + 1]) == type(field[min(cords_y[0]) + 1][min(cords_x[0]) + 1])) or (size == (3, 2) and type(field[min(cords_y[0]) + 1][min(cords_x[0])]) == type(field[min(cords_y[0]) + 1][min(cords_x[0]) + 1])))): # 2*2-es négyzet, opcionálisan max 1 elemmel valamelyik oldalon
        to_remove = same_elemets
        return (ShapeTypes.SMALL_BOMB, to_remove)
    elif 4 in cords_x[1]: # függőleges 4-es
        needed_x = cords_x[0][cords_x[1].index(4)]
        y_min = len(field)
        for i in same_elemets:
            if i[1] == needed_x and i[0] < y_min:
                y_min = i[0]
        for i in range(y_min, y_min + 4):
            to_remove.append((i, needed_x))
        return (ShapeTypes.FOUR_IN_ROW_V, to_remove)
    elif 4 in cords_y[1]: # vízszintes 4-es
        needed_y = cords_y[0][cords_y[1].index(4)]
        x_min = len(field[0])
        for i in same_elemets:
            if i[0] == needed_y and i[1] < x_min:
                x_min = i[1]
        for i in range(x_min, x_min + 4):
            to_remove.append((needed_y, i))
        return (ShapeTypes.FOUR_IN_ROW_H, to_remove)
    elif 3 in cords_x[1]: # függőleges 3-as
        needed_x = cords_x[0][cords_x[1].index(3)]
        y_min = len(field)
        for i in same_elemets:
            if i[1] == needed_x and i[0] < y_min:
                y_min = i[0]
        for i in range(y_min, y_min + 3):
            to_remove.append((i, needed_x))
        return (ShapeTypes.THREE_IN_ROW, to_remove)
    elif 3 in cords_y[1]: # víszintes 3-as
        needed_y = cords_y[0][cords_y[1].index(3)]
        x_min = len(field[0])
        for i in same_elemets:
            if i[0] == needed_y and i[1] < x_min:
                x_min = i[1]
        for i in range(x_min, x_min + 3):
            to_remove.append((needed_y, i))
        return (ShapeTypes.THREE_IN_ROW, to_remove)

    return (None, to_remove)

def arrange_field(field, field_size, moving_elements, corner, border):
    for i in range(field_size[1]): # most oszlopokat felügyelünk
        j = field_size[0] - 1
        while j >= 0: # az üres cellákba lemozgatjuk a felettük lévőket
            if field[j][i] == None:
                k = j - 1
                while k >= 0 and field[k][i] == None:
                    k -= 1
                if k >= 0:
                    field[j][i] = field[k][i]
                    field[k][i] = None
                    moving_elements.append(classes.Moving(field[j][i], (corner[0] + i * border.texture.get_width() + 3, corner[1] + j * border.texture.get_height() + 3), True))

            j -= 1

        count = 0
        j = field_size[0] - 1
        while j >= 0: # kitöltjük az üresen maradt cellékat felülről
            if field[j][i] == None:
                count += 1
                field[j][i] = random_party()()
                field[j][i].new_pos((corner[0] + i * border.texture.get_width() + 3, 0 - (count * border.texture.get_height() * 2 - 3)), False)
                moving_elements.append(classes.Moving(field[j][i], (corner[0] + i * border.texture.get_width() + 3, corner[1] + j * border.texture.get_height() + 3), True))

            j -= 1

def remove_tiles(field, side_one, side_two, etalon, sum_icon, nums, moving_elements):
    if side_two == None:
        sides = [side_one]
    else:
        sides = (side_one, side_two)
    for j in sides:
        if j[0] in ShapeTypes.ShapeDict:
            for i in j[1]:
                if type(field[i[0]][i[1]]) == type(etalon):
                    nums.etalon_num -= 1
                    moving_elements.append(classes.Moving(field[i[0]][i[1]], etalon.pos))
                else:
                    moving_elements.append(classes.Moving(field[i[0]][i[1]], sum_icon.pos))
                nums.all_num += 1
                field[i[0]][i[1]] = None

def can_move(field):
    radius = ((-1, 0), (0, -1), (1, 0), (0, 1))
    for i in range(len(field)):
        for j in range(len(field[i])):
            if isinstance(field[i][j], classes.Gadgets):
                return True
            for k in radius:
                try:
                    if i + k[0] < 0 or j + k[1] < 0:
                        raise ValueError
                    temp = field[i + k[0]][j + k[1]] # ha nincs ilyen, kivétel keletkezik
                    field[i + k[0]][j + k[1]] = field[i][j]
                    field[i][j] = temp
                    if not shape_analysis(field, collect_same(field, (i, j), (i, j), [ ]))[0] == None or not shape_analysis(field, collect_same(field, (i + k[0], j + k[1]), (i + k[0], j + k[1]), [ ]))[0] == None: # van-e lehetőség valamelyik oldalon
                        temp = field[i + k[0]][j + k[1]] # visszacserélünk
                        field[i + k[0]][j + k[1]] = field[i][j]
                        field[i][j] = temp
                        return True
                    temp = field[i + k[0]][j + k[1]] # visszacserélünk
                    field[i + k[0]][j + k[1]] = field[i][j]
                    field[i][j] = temp
                except:
                    pass
    return False

def reshuffle(field, field_size, corner, border, moving_elements):
    num_of_tiles = field_size[0] * field_size[1]
    for i in range(len(field)):
        for j in range(len(field[i])):
            rand_tile = random.randint(0, num_of_tiles - 1)
            rand_i = rand_tile // field_size[1]
            rand_j = rand_tile % field_size[1]
            temp = field[rand_i][rand_j]
            field[rand_i][rand_j] = field[i][j]
            field[i][j] = temp
    for i in range(len(field)):
        for j in range(len(field[i])):
            moving_elements.append(classes.Moving(field[i][j], (corner[0] + j * border.texture.get_width() + 3, corner[1] + i * border.texture.get_height() + 3), True))
