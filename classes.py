import pygame
import math

class Screen:
    resolution = (1280, 720)
    fps_options = (60, 90, 120)
    fps_index = 0
    blue = (56, 190, 235)
    purple = (81, 48, 105)

    def fps_step():
        Screen.fps_index = (Screen.fps_index + 1) % len(Screen.fps_options)

class Characters:
    def __init__(self, name = None, pic = None, score = 0):
        self.name = name
        self.pic = pic
        self.score = score

    def sort_key(self):
        return self.score

class CharacterData:
    characters = [ ]

    last_choice = 0

    def load(): # mert nem lehet convertálni, ameddig a pygame nem aktív, de ne itt töltsük be a PyGame-t
        CharacterData.characters = [
            Characters("A producer", pygame.image.load("Files/sgy.png").convert_alpha()),
            Characters("A főszereplő", pygame.image.load("Files/gyf.png").convert_alpha()),
            Characters("A bukott pártelnök", pygame.image.load("Files/fgya.png").convert_alpha()),
            Characters("A balfék haver", pygame.image.load("Files/kg.png").convert_alpha()),
            Characters("Az új kedvenc", pygame.image.load("Files/mzp.png").convert_alpha()),
            Characters("A feleség", pygame.image.load("Files/dk2.png").convert_alpha()),
            Characters("Régi ellenség (most legjobb barát)", pygame.image.load("Files/jp.png").convert_alpha())
        ]

    def return_scores():
        return [ i.score for i in CharacterData.characters ]

class Settings:
    music = True

    def save():
        with open("Data/data.txt", "wt", encoding="utf8") as f:
            f.write(f"{Screen.fps_index}\n")
            f.write(f"{Settings.music}\n")
            f.write(f"{' '.join([ str(i) for i in CharacterData.return_scores() ])}\n")
            f.write(f"{CharacterData.last_choice}\n")
 
    def load():
        with open("Data/data.txt", "rt", encoding="utf-8") as f:
            sor = int(f.readline())
            if sor < 0 or sor >= len(Screen.fps_options):
                raise ValueError("Hibás fájl!")
            else:
                Screen.fps_index = sor
            sor = f.readline().rstrip("\n")
            if sor == "True":
                Settings.music = True
            elif sor == "False":
                Settings.music = False
            else:
                raise ValueError("Hibás fájl!")
            sor = f.readline().rstrip("\n").split(" ")
            if not len(sor) == len(CharacterData.characters):
                raise ValueError("Hibás fájl!")
            for i in range(len(sor)):
                CharacterData.characters[i].score = int(sor[i])
            CharacterData.last_choice = int(f.readline().rstrip("\n"))
            if CharacterData.last_choice < 0 or CharacterData.last_choice >= len(CharacterData.characters):
                raise ValueError("Hibás fájl!")

class Moving:
    active_field_swap = 0
    def __init__(self, which, where, is_field_swap = False):
        self.which = which
        try:
            self.which.moving = True
            self.where = where
            temp_vector = ((-1) * (where[1] - which.pos[1]), where[0] - which.pos[0])
            lnko = math.gcd(temp_vector[0], temp_vector[1])
            if lnko == 0:
                self.vector = (temp_vector[0], temp_vector[1])
            else:
                self.vector = (temp_vector[0] // lnko, temp_vector[1] // lnko)
            if abs(self.vector[0]) < abs(self.vector[1]):
                self.by_x = True
            else:
                self.by_x = False
            if is_field_swap:
                self.field = True
                Moving.active_field_swap += 1
            else:
                self.field = False
        except:
            pass

class Numbers:
    def __init__(self, e_num = 0, a_num = 0, steps = 0):
        self.etalon_num = e_num
        self.all_num = a_num
        self.steps = steps

class Items:
    def __init__(self, surface = None, pos = None, middle = True):
        self.texture = surface
        if not pos == None:
            if middle:
                self.pos = (pos[0] - self.texture.get_width() // 2, pos[1] - self.texture.get_height() // 2)
            else:
                self.pos = pos
        else:
            self.pos = None
    
    def new_pos(self, pos, middle = True):
        if middle:
            self.pos = (pos[0] - self.texture.get_width() // 2, pos[1] - self.texture.get_height() // 2)
        else:
            self.pos = pos

class Tiles(Items):
    def __init__(self, surface = None, pos = None, middle = True):
        Items.__init__(self, surface, pos, middle)
        self.moving = False
        self.marked = False

class Parties(Tiles): # csak arra kell, hogy párt típusúak lehessenek az elemek
    def __init__(self, surface = None, pos = None, middle = True):
        Tiles.__init__(self, surface, pos, middle)

class Fidesz(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/fidesz.png").convert_alpha(), pos, middle)

class DK(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/dk.png").convert_alpha(), pos, middle)

class Jobbik(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/jobbik.png").convert_alpha(), pos, middle)

class LMP(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/lmp.png").convert_alpha(), pos, middle)

class MiHazank(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/mihazank.png").convert_alpha(), pos, middle)

class Momentum(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/momentum.png").convert_alpha(), pos, middle)

class MSZP(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/mszp.png").convert_alpha(), pos, middle)

class Parbeszed(Parties):
    def __init__(self, pos = None, middle = True):
        Parties.__init__(self, pygame.image.load("Files/parbeszed.png").convert_alpha(), pos, middle)

class Gadgets(Tiles): # csak arra kell, hogy segítség típusúak lehessenek az elemek
    def __init__(self, surface = None, pos = None, middle = True):
        Tiles.__init__(self, surface, pos, middle)

    def activate(self): # tisztán virtiális függvény
        raise NotImplementedError()

class h_rocket(Gadgets):
    def __init__(self, pos = None, middle = True):
        Gadgets.__init__(self, pygame.image.load("Files/h_rocket.png").convert_alpha(), pos, middle)
    
    def activate(self, field, cord, etalon, sum_icon, moving_elements, nums):
        for i in range(len(field[cord[0]])):
            if type(field[cord[0]][i]) == type(etalon):
                nums.etalon_num -= 1
                moving_elements.append(Moving(field[cord[0]][i], etalon.pos))
            elif isinstance(field[cord[0]][i], Gadgets):
                nums.all_num -= 1 # kompenzáljuk a későbbit, mert ez nem számít sehova, és nem is kell meganimálni a leszedését
            else:
                moving_elements.append(Moving(field[cord[0]][i], sum_icon.pos))
            nums.all_num += 1
            if isinstance(field[cord[0]][i], Gadgets):
                if not field[cord[0]][i].marked:
                    field[cord[0]][i].marked = True
                    field[cord[0]][i].activate(field, (cord[0], i), etalon, sum_icon, moving_elements, nums)
            field[cord[0]][i] = None

class v_rocket(Gadgets):
    def __init__(self, pos = None, middle = True):
        Gadgets.__init__(self, pygame.image.load("Files/v_rocket.png").convert_alpha(), pos, middle)

    def activate(self, field, cord, etalon, sum_icon, moving_elements, nums):
        for i in range(len(field)):
            if type(field[i][cord[1]]) == type(etalon):
                nums.etalon_num -= 1
                moving_elements.append(Moving(field[i][cord[1]], etalon.pos))
            elif isinstance(field[i][cord[1]], Gadgets):
                nums.all_num -= 1 # kompenzáljuk a későbbit, mert ez nem számít sehova, és nem is kell meganimálni a leszedését
            else:
                moving_elements.append(Moving(field[i][cord[1]], sum_icon.pos))
            nums.all_num += 1
            if isinstance(field[i][cord[1]], Gadgets):
                if not field[i][cord[1]].marked:
                    field[i][cord[1]].marked = True
                    field[i][cord[1]].activate(field, (i, cord[1]), etalon, sum_icon, moving_elements, nums)
            field[i][cord[1]] = None

class bomb(Gadgets):
    def __init__(self, pos = None, middle = True):
        Gadgets.__init__(self, pygame.image.load("Files/big_bomb.png").convert_alpha(), pos, middle)
    
    def activate(self, field, cord, etalon, sum_icon, moving_elements, nums):
        radius = ((-2, 0), (-1, -1), (-1, 0), (-1, 1), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (1, -1), (1, 0), (1, 1), (2, 0))
        for i in radius:
            act_cord = (cord[0] + i[0], cord[1] + i[1])
            try:
                if act_cord[0] < 0 or act_cord[1] < 0:
                    raise ValueError
                if type(field[act_cord[0]][act_cord[1]]) == type(etalon):
                    nums.etalon_num -= 1
                    moving_elements.append(Moving(field[act_cord[0]][act_cord[1]], etalon.pos))
                elif isinstance(field[act_cord[0]][act_cord[1]], Gadgets):
                    nums.all_num -= 1
                else:
                    moving_elements.append(Moving(field[act_cord[0]][act_cord[1]], sum_icon.pos))
                nums.all_num += 1
                if isinstance(field[act_cord[0]][act_cord[1]], Gadgets):
                    if not field[act_cord[0]][act_cord[1]].marked:
                        field[act_cord[0]][act_cord[1]].marked = True
                        field[act_cord[0]][act_cord[1]].activate(field, act_cord, etalon, sum_icon, moving_elements, nums)
                field[act_cord[0]][act_cord[1]] = None
            except: # mezőn kívülre esik
                pass

class s_bomb(Gadgets):
    def __init__(self, pos = None, middle = True):
        Gadgets.__init__(self, pygame.image.load("Files/small_bomb.png").convert_alpha(), pos, middle)

    def activate(self, field, cord, etalon, sum_icon, moving_elements, nums):
        radius = ((-1, 0), (0, -1), (0, 0), (0, 1), (1, 0))
        for i in radius:
            act_cord = (cord[0] + i[0], cord[1] + i[1])
            try:
                if act_cord[0] < 0 or act_cord[1] < 0:
                    raise ValueError
                if type(field[act_cord[0]][act_cord[1]]) == type(etalon):
                    nums.etalon_num -= 1
                    moving_elements.append(Moving(field[act_cord[0]][act_cord[1]], etalon.pos))
                elif isinstance(field[act_cord[0]][act_cord[1]], Gadgets):
                    nums.all_num -= 1
                else:
                    moving_elements.append(Moving(field[act_cord[0]][act_cord[1]], sum_icon.pos))
                nums.all_num += 1
                if isinstance(field[act_cord[0]][act_cord[1]], Gadgets):
                    if not field[act_cord[0]][act_cord[1]].marked:
                        field[act_cord[0]][act_cord[1]].marked = True
                        field[act_cord[0]][act_cord[1]].activate(field, act_cord, etalon, sum_icon, moving_elements, nums)
                field[act_cord[0]][act_cord[1]] = None
            except: # mezőn kívülre esik
                pass

class ShapeTypes:
    THREE_IN_ROW = 1
    FOUR_IN_ROW_V = 2
    FOUR_IN_ROW_H = 3
    SMALL_BOMB = 4
    BIG_BOMB = 5
    ShapeDict = {
        1: "THREE_IN_ROW",
        2: "FOUR_IN_ROW_V",
        3: "FOUR_IN_ROW_H",
        4: "SMALL_BOMB",
        5: "BIG_BOMB"
    }
    GadgetDict = {
        FOUR_IN_ROW_V: h_rocket,
        FOUR_IN_ROW_H: v_rocket,
        BIG_BOMB: bomb,
        SMALL_BOMB: s_bomb
    }
