import random
from typing import Any


def main():
    hra = Hra()
    print(hra._herni_deska.get_legal_moves([4, 6], "Cerna"))
    #print(hra._herni_deska.is_valid_move(18, 2))


class Hra:
    def __init__(self) -> None:
        self._herni_deska = Herni_Deska()
        self._herni_deska.vytvor_kameny()
        self._dvojkostka = Dvojkostka()
        print(self._herni_deska)
        # players
        # current_player


class Herni_Deska:
    def __init__(self) -> None:
        self._herni_pole = self.vytvor_herni_pole()

    @property
    def herni_pole(self) -> list:
        return self._herni_pole

    # cislo pole ???
    def vytvor_herni_pole(self) -> list:
        herni_pole = []
        for i in range(0, 24):
            herni_pole.append(Herni_Pole(i))
        return herni_pole

    # do budoucna předělat
    def vytvor_kameny(self) -> None:
        new_cerny_kameny = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
        new_bily_kameny = [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

        for i in range(len(new_cerny_kameny)):
            for _ in range(new_cerny_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Cerna", i))    

        for i in range(len(new_bily_kameny)):
            for _ in range(new_bily_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Bila", i)) 

    # do budoucna předělat
    def is_valid_move(self, stone_from: int, stone_to: int) -> bool:
        # valid move -> pokud je v poli 1 kámen nebo méně jak 5 kamenů stejné barvy (1 nebo 2-5 stejné barvy)
        # stone_from; stone_to => fixní pozice herního_pole
        if stone_to > len(self._herni_pole) - 1:
            return False
        prvni_pole = self._herni_pole[stone_from]
        druhy_pole = self._herni_pole[stone_to]
        if prvni_pole.get_velikost() == 0 or prvni_pole.cislo_pole == druhy_pole.cislo_pole:
            return False 
        return druhy_pole.get_velikost() <= 1 or (prvni_pole.get_kamen().barva_kamene == druhy_pole.get_kamen().barva_kamene and druhy_pole.get_velikost() < 5)  

    def get_legal_moves(self, list_posunu: list, hrac_na_tahu: Any) -> dict:
        # [4, 6] -> [4, 6, 10]
        # pokud NENI valid 4 a zároveň 6 -> NENI valid ani 10 
        # [2, 2, 2, 2] -> [2, 4, 6, 8] (2, původní 2 + 2)
        # pokud je valid 2 -> checknout 2+2, pokud je valid 2+2 -> checknout 2+2+2 atd...
        # = projetí pole, is_valid_move() a vrácení všechno možných tahů
        # list_posunu -> [4, 6],[4, 6, 10] or [2, 2, 2, 2],[2, 4, 6, 8]
        # list_posunu -> [4],[4] or [2, 2, 2],[2, 4, 6]  
        valid_moves = {}
        for pole in self._herni_pole:
            if pole.get_velikost() >= 1:
                if pole.get_kamen().barva_kamene == hrac_na_tahu:
                    list_of_moves = [] 
                    # pokud list_posunu obsahuje stejná čísla nebo 1 číslo
                    if len(set(list_posunu)) == 1: 
                        for posun in range(list_posunu[0], (len(list_posunu) * list_posunu[0]) + 1, list_posunu[0]):
                            #print(pole.cislo_pole + posun)
                            if self.is_valid_move(pole.cislo_pole, pole.cislo_pole + posun):
                                list_of_moves.append(pole.cislo_pole + posun)
                            else:
                                break
                    else:
                        for posun in list_posunu:
                            if self.is_valid_move(pole.cislo_pole, pole.cislo_pole + posun):
                                list_of_moves.append(pole.cislo_pole + posun)
                        if len(list_of_moves) != 0:
                            if self.is_valid_move(pole.cislo_pole, pole.cislo_pole + sum(list_posunu)):
                                list_of_moves.append(pole.cislo_pole + sum(list_posunu))
                    valid_moves[pole.cislo_pole] = list_of_moves
        return valid_moves

    def muze_byt_vyhozen(self, stone_from: int, stone_to: int) -> bool:
        pass

    def vyhod_kamen(self):
        pass

    def move_kamen(self, aktualni_pozice_kamene: int, nova_pozice_kamene: int) -> None:
        # pop kamen z pole1
        # pokud je v poli právě jeden kámen s opačnou barvou -> vyhodit 
        # push kamen do pol2
        # = využití is_valid_move(), muze_byt_vyhozen(), vyhod_kamen()
        pass

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

    def get_pozice_kamene(self) -> int:
        return self._historie[-1]

    def move_kamen(self, nova_pozice) -> None:
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
        if len(self._kameny) <= 5:
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


class Bar:
    pass


class Hrac:
    def __init__(self, barva_hrace) -> None:
        self._cisla_posunu = []
        self._barva_hrace = barva_hrace

    def __str__(self) -> str:
        return f"Tento hráč hraje za barvu {self._barva_hrace}"


class Konzolovy_Hrac(Hrac):
    pass


class AIHrac(Hrac):
    pass


class FileManager():
    pass


class StatisticsManager():
    pass


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


if __name__ == "__main__":
    main()
