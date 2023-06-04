import random
from typing import Any
import json


def main():
    prvni, druhy = nahodna_barva_hrace()
    protihrac = None
    vstup = input("'vrhcaby.json' k nacteni nebo 'nova hra' k nove hre: ")
    while vstup not in ['vrhcaby.json', 'nova hra']:
        vstup = input("Spatny vstup zkuste: 'vrhcaby.json' k nacteni nebo 'nova hra' k nove hre: ")
    if vstup == 'nova hra':
        jaky_protihrac = input("Hrat proti AI nebo clovek: ")
        while jaky_protihrac not in ['clovek', 'ai']:
            jaky_protihrac = input("Spatny vstup zkuste: AI nebo clovek: ")
        if jaky_protihrac.lower() == 'clovek':
            protihrac = Konzolovy_Hrac(prvni[0], prvni[1])
        elif jaky_protihrac.lower() == 'ai':
            protihrac = AIHrac(prvni[0], prvni[1])
        
        hrac = Konzolovy_Hrac(druhy[0], druhy[1])
        hra = Hra(pridej_hrace(hrac, protihrac))
    else:
        # load hry
        pass

def save_file():
    pass


def load_file():
    pass


def nahodna_barva_hrace() -> str:
    seznam = [("Bila", 25), ("Cerna", 0)]
    random.shuffle(seznam)
    return seznam

def pridej_hrace(hrac1, hrac2) -> list:
    hraci = []
    if hrac1.barva_hrace == "Bila":
        hraci.append(hrac1)
        hraci.append(hrac2)
    else:
        hraci.append(hrac2)
        hraci.append(hrac1)
    return hraci


class Hra:
    def __init__(self, hraci: Any) -> None:
        self._herni_deska = Herni_Deska()
        self._herni_deska.vytvor_kameny()
        self._dvojkostka = Dvojkostka()
        self._hraci = hraci
        self._current_player = 0
        self._zapni_hru = True
        self.zapni_hru()

    def zapni_hru(self) -> None:
        while self._zapni_hru:
            self.zacatek_novyho_tahu()
        else:
            self.vypis_statistiky(self._hraci, self._herni_deska.herni_pole)

    def zacatek_novyho_tahu(self) -> None:    
        curr_player = self._hraci[self._current_player]
        vysledek_kostky = self._dvojkostka.hod_dvojkostkou()
        #vysledek_kostky = [1,1,1,1]
        list_posunu = self.modify_list_posunu(curr_player.barva_hrace, list(vysledek_kostky))
        legal_moves = self.get_legal_moves(list_posunu, self._hraci[self._current_player])
        self.vypis_hru(curr_player, self._hraci[self.next_player()], vysledek_kostky, list_posunu, legal_moves)

        while len(list_posunu) != 0 and self._zapni_hru:
            
            if not any(legal_moves.values()):
                print("ZADNY MOZNY TAH")
                break
            
            # str, str, list[int, int]
            tah = curr_player.hrat_tah(legal_moves)

            if tah == "ukoncit":
                self._zapni_hru = False
                break
            if tah == "ulozit":
                self.ulozit_hru()

            aktulani_pozice, nova_pozice = tah
            # odečetení od listu_posunu
            vzdalenost = nova_pozice - aktulani_pozice
            if vzdalenost in list_posunu:
                # JINEJ MOVE PRI MOVE Z BARU
                self._herni_deska.presun_kamen(aktulani_pozice, nova_pozice, curr_player, self._hraci[self.next_player()])
                    
                list_posunu.remove(vzdalenost)
            else:
                if len(set(list_posunu)) == 1:
                    pocet = vzdalenost / list_posunu[0]
                    while pocet > 0:
                        nova_pozice = legal_moves.get(aktulani_pozice)[0]
                        #print(f"{budouci_pozice, aktulani_pozice}")
                        #print(f"LEGAL MOVES: {legal_moves.get(aktulani_pozice)}")
                        self._herni_deska.presun_kamen(aktulani_pozice, nova_pozice, curr_player, self._hraci[self.next_player()])
                        list_posunu.remove(nova_pozice - aktulani_pozice)
                        aktulani_pozice = nova_pozice
                        legal_moves = self.get_legal_moves(list_posunu, curr_player)
                        pocet -= 1
                else:
                    while len(list_posunu) != 0:
                        nova_pozice = legal_moves.get(aktulani_pozice)[0]
                        #print(f"{budouci_pozice, aktulani_pozice}")
                        #print(f"LEGAL MOVES: {legal_moves.get(aktulani_pozice)}")
                        self._herni_deska.presun_kamen(aktulani_pozice, nova_pozice, curr_player, self._hraci[self.next_player()])
                        list_posunu.remove(nova_pozice - aktulani_pozice)
                        aktulani_pozice = nova_pozice
                        legal_moves = self.get_legal_moves(list_posunu, curr_player)
                
            legal_moves = self.get_legal_moves(list_posunu, curr_player)
            self.vypis_hru(curr_player, self._hraci[self.next_player()], vysledek_kostky, list_posunu, legal_moves)    
        else:
            self._current_player = self.next_player()
            # novy tah

    def vypis_hru(self, curr_player: Any, next_player: Any, vysledek_kostky: list, list_posunu: list, legal_moves: dict) -> None:
        print("---------------------------------------------------------")
        print(f"{next_player} {next_player.bar}")
        print(self._herni_deska)
        print(f"{curr_player} {curr_player.bar}")
        print(f"Na tahu je {curr_player.barva_hrace}")
        print(f"Cisla na kostce: {vysledek_kostky}, posuny: {list_posunu}")
        print(f"Mozne tahy: {legal_moves}")
        print("---------------------------------------------------------")

    def vypis_statistiky(self, hraci, herni_pole):
        # pocet - vyhozenych, vyvedenych, opustenych kamenu
        print("---------------------------------------------------------")
        print("STATISTIKY")
        for hrac in hraci:
            print(f"Barva hrace: {hrac.barva_hrace}")
            print(f"Bylo vyhozeno: {hrac.vyhozeno_kamenu}")
            print(f"Vyvedeno kamenu: {herni_pole[hrac.index_domecku()].get_velikost()}")
            print(f"Opusteno kamenu: {15 - herni_pole[hrac.index_domecku()].get_velikost()}")
            print("------------")
        print("---------------------------------------------------------")
        ukoncit_hru = input("Pro ukonceni napiste 'ukoncit': ")
        while ukoncit_hru != "ukoncit":
            ukoncit_hru = input("Pro ukonceni napiste 'ukoncit': ")

    def ulozit_hru(self):
        pass

    def next_player(self):
        return (self._current_player + 1) % len(self._hraci)

    def get_legal_moves(self, list_posunu: list, hrac: Any) -> dict:
        return self._herni_deska.get_legal_moves(list_posunu, hrac)

    def modify_list_posunu(self, barva_hrace: str, list_posunu: int) -> list:
        return [-x for x in list_posunu] if barva_hrace == "Bila" else list_posunu

class Herni_Deska:
    def __init__(self) -> None:
        self._herni_pole = self.vytvor_herni_pole()

    @property
    def herni_pole(self) -> list:
        return self._herni_pole

    def vytvor_herni_pole(self) -> list:
        herni_pole = []
        herni_pole.append(Domecek(0, 15))
        for i in range(1, 24+1):
            herni_pole.append(Herni_Pole(i))
        herni_pole.append(Domecek(25, 15))
        return herni_pole

    def vytvor_kameny(self) -> None:
        #kameny = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0]
        kameny = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(kameny)):
            for _ in range(kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Cerna", i))
                    self._herni_pole[len(kameny) - i - 1].vloz_kamen(Kamen("Bila", i))    
   
    def presun_kamen(self, aktualni_pozice: int, nova_pozice: int, hrac, protihrac) -> None:
        kamen1 = None
        if aktualni_pozice == hrac.bar.cislo_pole:
            kamen1 = hrac.bar.vytahni_kamen()
            kamen1.vymaz_historii()
        else:
            kamen1 = self._herni_pole[aktualni_pozice].vytahni_kamen()

        if self.muze_byt_vyhozen(kamen1.barva_kamene, nova_pozice):
            self.vyhod_kamen(nova_pozice, protihrac)

        self._herni_pole[nova_pozice].vloz_kamen(kamen1)
        kamen1.zapis_pozici_do_historie(nova_pozice)    

    def get_legal_moves(self, list_posunu: list, hrac: Any) -> dict:
        # list_posunu -> [4, 6],[4, 6, 10] or [2, 2, 2, 2],[2, 4, 6, 8]
        # list_posunu -> [4],[4] or [2, 2, 2],[2, 4, 6]  
        valid_moves = {}
        # pokud je v baru kámen
        if hrac.bar.get_velikost() > 0:
            valid_moves["Bar"] = self.calculate_legal_moves(hrac.bar.cislo_pole, list_posunu, hrac.barva_hrace)
        else:
            for pole in self._herni_pole[1:-1]:
                if pole.get_velikost() >= 1:
                    if pole.get_kamen().barva_kamene == hrac.barva_hrace:
                        valid_moves[pole.cislo_pole] = self.calculate_legal_moves(pole.cislo_pole, list_posunu, hrac.barva_hrace)
        return valid_moves
    
    def calculate_legal_moves(self, cislo_pole: int, list_posunu: list, hrac_na_tahu: str) -> list:
        list_of_moves = [] 
        # pokud list_posunu obsahuje stejná čísla nebo 1 číslo
        if len(set(list_posunu)) == 1:                                           
            posuny = [x * list_posunu[0] for x in range(1, len(list_posunu)+1)]
            for posun in posuny:
                if self.is_valid_move(cislo_pole + posun, hrac_na_tahu):
                    list_of_moves.append(cislo_pole + posun)
                else:
                    break
        else:
            for posun in list_posunu:
                if self.is_valid_move(cislo_pole + posun, hrac_na_tahu):
                    list_of_moves.append(cislo_pole + posun)
            if len(list_of_moves) != 0:
                if self.is_valid_move(cislo_pole + sum(list_posunu), hrac_na_tahu):
                    list_of_moves.append(cislo_pole + sum(list_posunu))
        return list_of_moves

    def is_valid_move(self, stone_to: int, barva_hrace: str) -> bool:
        if stone_to < 0 or stone_to > len(self._herni_pole) - 1:
            return False
        if stone_to in [0, 25] and self.muze_jit_do_domecku(barva_hrace):
            return True
        elif not stone_to in [0, 25]:
            druhy_pole = self._herni_pole[stone_to]
            return druhy_pole.get_velikost() <= 1 or (barva_hrace == druhy_pole.get_kamen().barva_kamene and druhy_pole.get_velikost() < 5)

    # PREDELAT
    def muze_jit_do_domecku(self, barva_hrace: str) -> bool:
        # checknout jestli jsou v posledním kvadrantu všechny kameny
        # only in 1-6 white
        # only in 19-24 black
        if barva_hrace == "Bila":
            for pole in self._herni_pole[1:-1]:
                if not pole.je_prazdny():
                    if pole.get_kamen().barva_kamene == barva_hrace:
                        if pole.cislo_pole > 6:
                            return False
            return True
        else:
            for pole in self._herni_pole[1:-1]:
                if pole.get_velikost() >= 1:
                    if pole.get_kamen().barva_kamene == barva_hrace:
                        if pole.cislo_pole < 19:
                            #print("INVALID MOVE")
                            return False
            return True

    def muze_byt_vyhozen(self, barva_kamene: str, stone_to: int) -> bool:
        druhy_pole = self._herni_pole[stone_to]
        return druhy_pole.get_velikost() == 1 and barva_kamene != druhy_pole.get_kamen().barva_kamene

    def vyhod_kamen(self, pozice_kamene: int, hrac) -> None:
        kamen = self._herni_pole[pozice_kamene].vytahni_kamen()
        hrac.bar.vloz_kamen(kamen)
        hrac.zvys_pocet_vyhozeno_kamenu()
        kamen.zapis_pozici_do_historie("Bar")
        print("Kamen byl vyhozen")

    def __str__(self) -> str:
        return "\n".join(str(pole) for pole in self._herni_pole)


class Kamen:
    def __init__(self, barva_kamene: str, pozice_kamene: int) -> None:
        self._barva_kamene = barva_kamene
        self._historie = []
        self._historie.append(pozice_kamene)

    @property
    def barva_kamene(self) -> str:
        return self._barva_kamene

    @property
    def historie(self) -> list:
        return self._historie

    def vymaz_historii(self) -> None:
        self._historie = self._historie[-1:]

    def get_pozice_kamene(self) -> int:
        return self._historie[-1]

    def zapis_pozici_do_historie(self, nova_pozice: Any) -> None:
        self._historie.append(nova_pozice)

    def __str__(self) -> str:
        return f"{self._barva_kamene}"


# modifikovany zasobnik
class Herni_Pole:
    def __init__(self, i: int, max_size=5) -> None:
        self._cislo_pole = i
        self._kameny = []
        self._max_size = max_size

    def vloz_kamen(self, kamen: Kamen) -> None:
        if len(self._kameny) <= self._max_size:
            self._kameny.append(kamen)

    def vytahni_kamen(self) -> Kamen:
        if len(self._kameny):
            return self._kameny.pop()

    def get_kamen(self) -> Kamen:
        if len(self._kameny):
            return self._kameny[-1]

    def je_prazdny(self) -> bool:
        return len(self._kameny) == 0

    def get_velikost(self) -> int:
        return len(self._kameny)

    @property
    def cislo_pole(self) -> int:
        return self._cislo_pole
    
    @property
    def kameny(self) -> list:
        return self._kameny

    def __str__(self) -> str:
        return f"{self._cislo_pole}: {[str(kamen) for kamen in self._kameny]}"


class Bar(Herni_Pole):
    def __init__(self, i: int, max_size: int) -> None:
        super().__init__(i, max_size)

    def __str__(self) -> str:
        return f"bar: {self.get_velikost()}"
    

class Domecek(Herni_Pole):
    def __init__(self, i: int, max_size: int) -> None:
        super().__init__(i, max_size)

    def __str__(self) -> str:
        return f"Home: {self.get_velikost()}"


class Hrac:
    def __init__(self, barva_hrace, index_baru, vyhozeno_kamenu=0) -> None:
        self._barva_hrace = barva_hrace
        self._bar = Bar(index_baru, 15)
        self._vyhozeno_kamenu = vyhozeno_kamenu

    @property
    def vyhozeno_kamenu(self):
        return self._vyhozeno_kamenu
    
    def zvys_pocet_vyhozeno_kamenu(self):
        self._vyhozeno_kamenu += 1

    @property
    def barva_hrace(self) -> str:
        return self._barva_hrace
    
    @property
    def bar(self) -> Bar:
        return self._bar
    
    def index_domecku(self) -> int:
        return 0 if self._bar.cislo_pole == 25 else 25

    def __str__(self) -> str:
        return f"{self._barva_hrace}"


class Konzolovy_Hrac(Hrac):
    def __init__(self, barva_hrace, index_baru) -> None:
        super().__init__(barva_hrace, index_baru)

    def hrat_tah(self, legal_moves: dict) -> Any:
        tah = check_input(input("Zadej tah: ").split(','))
        while True:
            if tah[0] in ["ukoncit", "ulozit"]:
                return tah[0]
            for key, values in legal_moves.items():
                if tah[0] == key and tah[1] in values:
                    if tah[0] == "Bar":
                        return [self.bar.cislo_pole, tah[1]]
                    return tah 
            else:
                tah = check_input(input("Nelegální tah, zadejte tah znovu: ").split(','))


class AIHrac(Hrac):
    def __init__(self, barva_hrace, index_baru) -> None:
        super().__init__(barva_hrace, index_baru)

    def hrat_tah(self, legal_moves: dict) -> list:
        random_key = random.choice(list(legal_moves.keys()))
        random_value = random.choice(legal_moves.get(random_key))
        if random_key == "Bar":
            random_key = self.bar.cislo_pole
        return [random_key, random_value]  


class Dvojkostka:
    def __init__(self) -> None:
        pass

    def hod_dvojkostkou(self) -> list:
        prvni_hod = random.randint(1, 6)
        druhy_hod = random.randint(1, 6)
        if prvni_hod == druhy_hod:
            return [prvni_hod for _ in range(4)]
        else:
            return [prvni_hod, druhy_hod]


def check_input(items: list) -> list:
    result = []
    for item in items:
        try:
            result.append(int(item))
        except ValueError:
            result.append(item)
    return result


if __name__ == "__main__":
    main()
