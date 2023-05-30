import random
from typing import Any


def main():
    x = input("Cesta k JSON nebo napsat 'nova hra' k nove hre: ")
    # if x == '':
    # jaky_protihrac = input("Hrat proti AI/PC:" )
    # if jaky_protihrac.lower() == 'AI':
    hrac = Konzolovy_Hrac("Cerna")
    protihrac = Konzolovy_Hrac("Bila")
    hra = Hra(hrac, protihrac)
    # LOAD / NOVA HRA
    # NOVA HRA -> VYTVORIT HRACE -> AI/PC
    #hra._herni_deska._bar.vloz_kamen_do_baru("Cerna")
    #print(hra._herni_deska.get_legal_moves([2, 5], "Cerna"))
    #hra._herni_deska.move_kamen(0, 3)
    #print(hra._herni_deska.is_valid_move(18, 2))

def nahodna_barva_hrace() -> str:
    return random.choices(["Cerna", "Bila"])

class Hra:
    def __init__(self, hrac, protihrac) -> None:
        self._herni_deska = Herni_Deska()
        self._herni_deska.vytvor_kameny()
        self._dvojkostka = Dvojkostka()
        self._hraci = [hrac, protihrac]
        self._current_player = 0
        self.game_on()

    def game_on(self):
        while True:
            self.tah()

    def tah(self):
        print(self._herni_deska)
        barva_hrace = self._hraci[self._current_player].barva_hrace
        print(f"Na tahu je {barva_hrace}")
        vysledek_kostky = self._dvojkostka.hod_dvojkostkou()
        print(f"Cisla na kostce: {vysledek_kostky}")
        print(f"Mozne tahy: {self._herni_deska.get_legal_moves(vysledek_kostky, barva_hrace)}")
        input("Zadejte tah: ")


class Herni_Deska:
    def __init__(self) -> None:
        self._herni_pole = self.vytvor_herni_pole()
        self._bar = Bar()

    @property
    def herni_pole(self) -> list:
        return self._herni_pole

    def vytvor_herni_pole(self) -> list:
        herni_pole = []
        for i in range(24):
            herni_pole.append(Herni_Pole(i))
        return herni_pole

    # do budoucna předělat
    def vytvor_kameny(self) -> None:
        new_cerny_kameny = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
        new_bily_kameny = [0, 0, 1, 0, 0, 5, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

        for i in range(len(new_cerny_kameny)):
            for _ in range(new_cerny_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Cerna", i))    

        for i in range(len(new_bily_kameny)):
            for _ in range(new_bily_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Bila", i)) 

    def move_kamen(self, aktualni_pozice_kamene: int, nova_pozice_kamene: int) -> None:
        # pop kamen z pole1
        # pokud je v poli právě jeden kámen s opačnou barvou -> vyhodit 
        # push kamen do pol2
        if self.is_valid_move(aktualni_pozice_kamene, nova_pozice_kamene):
            kamen1 = self._herni_pole[aktualni_pozice_kamene].vytahni_kamen()
            if self.muze_byt_vyhozen(aktualni_pozice_kamene, nova_pozice_kamene):
                self.vyhod_kamen(nova_pozice_kamene)
            self._herni_pole[nova_pozice_kamene].vloz_kamen(kamen1)
            kamen1.zapis_pozici_do_historie(nova_pozice_kamene)
        pass

    def is_valid_move(self, aktualni_pozice_kamene: int, nova_pozice_kamene: int):
        pass

    def is_in_legal_moves(self, dict_moves: dict):
        pass

    def get_legal_moves(self, list_posunu: list, hrac_na_tahu: str) -> dict:
        # list_posunu -> [4, 6],[4, 6, 10] or [2, 2, 2, 2],[2, 4, 6, 8]
        # list_posunu -> [4],[4] or [2, 2, 2],[2, 4, 6]  
        valid_moves = {}
        # pokud je v baru kámen
        if self._bar.vrat_pocet_kamenu_v_baru(hrac_na_tahu) > 0:
            # pole je 0 nebo len(self._herni_deksa)
            valid_moves["Bar"] = self.calculate_legal_moves(-1, list_posunu, hrac_na_tahu)
        else:
            for pole in self._herni_pole:
                if pole.get_velikost() >= 1:
                    if pole.get_kamen().barva_kamene == hrac_na_tahu:
                        valid_moves[pole.cislo_pole] = self.calculate_legal_moves(pole.cislo_pole, list_posunu, hrac_na_tahu)
        return valid_moves
    
    def calculate_legal_moves(self, cislo_pole: int, list_posunu: list, hrac_na_tahu: str) -> list:
        list_of_moves = [] 
        # pokud list_posunu obsahuje stejná čísla nebo 1 číslo
        if len(set(list_posunu)) == 1:                                            # -1 
            for posun in range(list_posunu[0], (len(list_posunu) * list_posunu[0]) + 1, list_posunu[0]):
                # print(pole.cislo_pole + posun)
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
        if stone_to > len(self._herni_pole) - 1 or stone_to < 0:
            return False
        druhy_pole = self._herni_pole[stone_to]
        return druhy_pole.get_velikost() <= 1 or (barva_hrace == druhy_pole.get_kamen().barva_kamene and druhy_pole.get_velikost() < 5)  

    def muze_byt_vyhozen(self, stone_from: int, stone_to: int) -> bool:
        prvni_pole = self._herni_pole[stone_from]
        druhy_pole = self._herni_pole[stone_to]
        return druhy_pole.get_velikost() == 1 and prvni_pole.get_kamen().barva_kamene != druhy_pole.get_kamen().barva_kamene

    def vyhod_kamen(self, pozice_kamene) -> None:
        kamen = self._herni_pole[pozice_kamene].vytahni_kamen()
        self._bar.vloz_kamen_do_baru(kamen.barva_kamene)
        print(self._bar._bily_kameny)

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


class Bar:
    def __init__(self) -> None:
        self._bily_kameny = []
        self._cerny_kameny = []

    def vloz_kamen_do_baru(self, barva) -> None:
        if barva == "Cerna":
            self._cerny_kameny.append(Kamen("Cerna", "Bar"))
        else:
            self._bily_kameny.append(Kamen("Bila", "Bar"))

    def vrat_pocet_kamenu_v_baru(self, barva):
        return len(self._bily_kameny) if barva == "Bila" else len(self._cerny_kameny)

    def vrat_bily_kamen(self) -> Kamen:
        pass
        #return Kamen("")

    def vrat_cerny_kamen(self) -> Kamen:
        pass
        #return Kamen("")

    def __str__(self) -> str:
        return f"Na baru je {len(self._bily_kameny)} bilých a {len(self._cerny_kameny)} černých kamenů"


class Hrac:
    def __init__(self, barva_hrace) -> None:
        self._cisla_posunu = []
        self._barva_hrace = barva_hrace

    @property
    def barva_hrace(self):
        return self._barva_hrace

    def __str__(self) -> str:
        return f"Tento hráč hraje za barvu {self._barva_hrace}"


class Konzolovy_Hrac(Hrac):
    def __init__(self, barva_hrace) -> None:
        super().__init__(barva_hrace)


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
