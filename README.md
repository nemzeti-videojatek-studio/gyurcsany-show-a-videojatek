# A Gyurcsány-show: A videójáték
Közeleg a választások napja, így Gyurcsány Ferenc is nekiáll szavazatokat gyűjteni. Segíts neki benne, és bújj kedvenc szereplőd bőrébe! Jobb oldalt látod, hogy éppen melyik párt támogatóinak szavazataira fáj leginkább a foga (Igen, néha még a DK-sokat is meg kell erősíteni a hitükben!), és hogy hány darabra. Emellett Feri természetesen minden más szavazatnak is örül. De vigyázz, csak korlátozott lépéseid vannak! Ha ezek elfogynak, honatyáink észreveszik, hogy segítesz neki balliberális propagandát terjeszteni, és mindenkit visszaterelnek a helyes útra.

## Játékmenet:
Ami ismeri a Candy Crush-t vagy a Homescapest, annak nem fog nagy meglepetést okozni. Szomszédos elemeket kell kicserélni húzással vagy kattintással olyan módon, hogy legalább 3 darab egyforma elemet tegyél egymás mellé. A játék akkor ér véget, ha elfogytak a lépéseid vagy összegyűjtötted a szükséges mennyiséget a megadott pártlogóból. A kütyük cserére vagy dupla kattintásra aktiválódnak.
 - 3 egy vonalban: Semmi, egyszerűen csak eltűnik és bezsebeli a szavazatokat.
 - 4 egy vonalban, vízszintesen: A helyén 1 darab függőleges rakéta jelenik meg, ami eltűnteti a vele egy oszlopban lévő elemeket.
 - 4 egy vonalban, függőlegesen: Analóg módon az előzővel, vízszintes rakétát ad.
 - 2*2-es négyzet (akár 1 db plusz elem valamelyik oldalon): Kis bomba, aktiváláskor kitörli a közvetlen szomszédait.
 - Legalább 5 összefüggő darab T, L vagy I alakban: Nagy bomba, a kis bombához képest eggyel nagyobb sugárban robbant.
### Képernyőképek
![1](https://user-images.githubusercontent.com/96190894/146949910-261dd5ad-9fc4-4819-be54-e48dabdc373d.jpg)
![2](https://user-images.githubusercontent.com/96190894/146949916-229c65fa-525a-4b3a-804c-8a91a319508f.jpg)
![3](https://user-images.githubusercontent.com/96190894/146949922-d1e01eec-b00a-4be2-85bf-ad7330168eba.jpg)
![4](https://user-images.githubusercontent.com/96190894/146949933-06f1a12f-0fd2-47c0-aba7-8209878182f2.jpg)
![5](https://user-images.githubusercontent.com/96190894/146949942-ba810c26-decf-416d-93df-bb96e4dcf7d4.jpg)

## Pontozás:
Ha sikerült teljesíteni a játék által generált feladatot, a játék előtt kiválasztott karakter pontszámához hozzáadódik az összes leszedett pártlogó száma, a karakterek ezalapján kerülnek rangsorolásra.

## Letöltés:
A releases rész alatt megtalálod a neked megfelelő csomagot: https://github.com/nemzeti-videojatek-studio/gyurcsany-show-a-videojatek/releases

## Futtatás:
Windows alatt a feri_32.exe vagy a feri_64.exe fájlt indítsd el!

Ha nem bízol az általam fordított verzióban, vagy más rendszert használsz, futtathatod közvetlenül a forrásfájlokat is:

Ha tudod, mi az a Python és a PyGame, a main.pyw fájlt indítsd el.
### A többieknek:
Ez a program Python 3.9 nyelven íródott, a PyGame modulra építve, először ezeket kell telepítened.
#### Windows:
 - Töltsd le a Pythont a hivatalos weboldalról: https://www.python.org/
 - A telepítés során pipáld be az "Add Python to PATH" sort.
 - Telepítés után nyisd meg a parancssort vagy a PowerShellt és írd be a következőt: pip install pygame
 - Ezután már készenállsz a játékra, nyisd meg a main.pyw fájlt.
#### Linux:
Néhány disztribúció már alapból tartalmazza a Pythont, például Ubuntu esetében a következő lépésekre van szükség:
 - Nyisd meg a terminált, és telepítsd a PIP-et, ezzel tudod telepíteni a PyGame modult a Pythonhoz:
 - sudo apt install python3-pip
 - Ha ez kész, telepítheted a PyGame-t:
 - pip install pygame
 - Ezután navigálj a letöltött játék mappájába vagy nyiss meg egy másik terminált a fájlkezelőn keresztül, a játék mappájában jobb egérgombbal a "Terminál megnyitása itt" opcióval.
 - Indítsd el a main.pyw-t:
 - python3 main.pyw
#### macOS:
 - Sajnos nem tudok segíteni, de a Python hivatalos oldalán letölthető a telepítő macOS-re is, így valószínűleg hasonló a Windows-os módszerhez.

## Megjegyzés:

Ez a program kizárólag szórakoztatási céllal jött létre. Nem célja senki politikai véleményének befolyásolása vagy megsértése.

A forráskód felhasználása nem engedélyköteles, egyedül annyit kérek, hogy valamilyen módon hivatkozz erre a projektre, például a GitHub projekt linkjével. A kiadás után tőlem hivatalos frissítés nem várható.

## Felhasznált anyagok:
### Háttér és zene:

https://youtu.be/ZfV5Xr47ggU

Innen is köszönöm a feltöltőnek! :)
### Betűtípus:
Mistral

### Pártlogók:
#### Az ellenzéki összefogásban résztvevő pártok:
https://elovalasztas2021.hu/
#### Mi Hazánk:
https://hu.wikipedia.org/wiki/Mi_Haz%C3%A1nk_Mozgalom
#### Fidesz:
https://hu.wikipedia.org/wiki/Fidesz_%E2%80%93_Magyar_Polg%C3%A1ri_Sz%C3%B6vets%C3%A9g

Jó szórakozást mindenkinek, és ha ismersz valakit, akinek tetszene ez a játék, oszd meg vele is! :)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licenc" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Ez a Mű a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Nevezd meg! - Ne add el! - Így add tovább! 4.0 Nemzetközi Licenc</a> feltételeinek megfelelően felhasználható.
