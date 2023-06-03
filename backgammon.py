import random
from typing import Any


def main():
    x = input("Cesta k JSON nebo napsat 'nova hra' k nove hre: ")
    # if x == '':
    # jaky_protihrac = input("Hrat proti AI/PC:" )
    # if jaky_protihrac.lower() == 'AI':
    hrac = Konzolovy_Hrac("Cerna", 0)
    protihrac = Konzolovy_Hrac("Bila", 25)
    hra = Hra(hrac, protihrac)
    # LOAD / NOVA HRA

def nahodna_barva_hrace() -> str:
    return random.choices(["Cerna", "Bila"])


class Hra:
    def __init__(self, hrac: Any, protihrac: Any) -> None:
        self._herni_deska = Herni_Deska()
        self._herni_deska.vytvor_kameny()
        self._dvojkostka = Dvojkostka()
        self._hraci = [hrac, protihrac]
        self._current_player = 0
        self._zapni_hru = True
        self.game_on()

    def game_on(self) -> None:
        while self._zapni_hru:
            self.zacatek_novyho_tahu()

    def zacatek_novyho_tahu(self) -> None:    
        curr_player = self._hraci[self._current_player]
        # vysledek_kostky = self._dvojkostka.hod_dvojkostkou()
        vysledek_kostky = [1, 2]
        list_posunu = self.modify_list_posunu(curr_player.barva_hrace, list(vysledek_kostky))
        legal_moves = self.get_legal_moves(list_posunu, self._hraci[self._current_player])
        self.vypis_hru(curr_player, vysledek_kostky, list_posunu, legal_moves)

        while len(legal_moves) != 0 and len(list_posunu) != 0:
            # hracuv tah je legalni
            curr_player = self._hraci[self._current_player]
            hracuv_tah = curr_player.hrat_tah(legal_moves)
            
            # odečetení od listu_posunu
            vzdalenost = hracuv_tah[1] - hracuv_tah[0]
            if vzdalenost in list_posunu:
                # JINEJ MOVE PRI MOVE Z BARU
                self._herni_deska.move_kamen(hracuv_tah[0], hracuv_tah[1], curr_player, self._hraci[self.next_player()])
                    
                list_posunu.remove(vzdalenost)
            else:
                # komplexní move() (více jak 2x move)
                self._herni_deska.is_valid_move()
                pass
                
            legal_moves = self.get_legal_moves(list_posunu, curr_player)
            self.vypis_hru(curr_player, vysledek_kostky, list_posunu, legal_moves)    
        else:
            self._current_player = self.next_player()
            # novy tah

    def vypis_hru(self, curr_player: Any, vysledek_kostky: list, list_posunu: list, legal_moves: dict) -> None:
        print("---------------------------------------------------------")
        print(self._herni_deska)
        print(curr_player.bar)
        print(f"Na tahu je {curr_player.barva_hrace}")
        print(f"Cisla na kostce: {vysledek_kostky}, posuny: {list_posunu}")
        print(f"Mozne tahy: {legal_moves}")
        print("---------------------------------------------------------")

    def next_player(self):
        return (self._current_player + 1) % len(self._hraci)

    def get_legal_moves(self, list_posunu: list, hrac: Any) -> dict:
        return self._herni_deska.get_legal_moves(list_posunu, hrac)

    def modify_list_posunu(self, barva_hrace: str, list_posunu: int) -> list:
        return [-x for x in list_posunu] if barva_hrace == "Bila" else list_posunu


class Herni_Deska:
    def __init__(self) -> None:
        self._herni_pole = self.vytvor_herni_pole()

    def vytvor_herni_pole(self) -> list:
        herni_pole = []
        herni_pole.append(Domecek(0, 15))
        for i in range(1, 24+1):
            herni_pole.append(Herni_Pole(i))
        herni_pole.append(Domecek(25, 15))
        return herni_pole

    def vytvor_kameny(self) -> None:
        #kameny = [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0]
        kameny = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0]
        for i in range(len(kameny)):
            for _ in range(kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Cerna", i))
                    self._herni_pole[len(kameny) - i - 1].vloz_kamen(Kamen("Bila", i))    
   
    def move_kamen(self, aktualni_pozice: int, nova_pozice: int, hrac, protihrac) -> None:
        kamen1 = None
        if aktualni_pozice == hrac.bar.cislo_pole:
            kamen1 = hrac.bar.vytahni_kamen()
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
                            print("INVALID MOVE")
                            return False
            return True

    def muze_byt_vyhozen(self, barva_kamene: str, stone_to: int) -> bool:
        druhy_pole = self._herni_pole[stone_to]
        return druhy_pole.get_velikost() == 1 and barva_kamene != druhy_pole.get_kamen().barva_kamene

    def vyhod_kamen(self, pozice_kamene: int, hrac) -> None:
        kamen = self._herni_pole[pozice_kamene].vytahni_kamen()
        hrac.bar.vloz_kamen(kamen)

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


class Bar(Herni_Pole):
    def __init__(self, i: int, max_size: int) -> None:
        super().__init__(i, max_size)

    def __str__(self) -> str:
        return f"Na baru je {self.get_velikost()} kamenů"
    

class Domecek(Herni_Pole):
    def __init__(self, i: int, max_size: int) -> None:
        super().__init__(i, max_size)

    def __str__(self) -> str:
        return f"Home: {self.get_velikost()}"


class Hrac:
    def __init__(self, barva_hrace, index_baru) -> None:
        self._barva_hrace = barva_hrace
        self._bar = Bar(index_baru, 15)

    @property
    def barva_hrace(self) -> str:
        return self._barva_hrace
    
    @property
    def bar(self) -> Bar:
        return self._bar

    def __str__(self) -> str:
        return f"Tento hráč hraje za barvu {self._barva_hrace}"


class Konzolovy_Hrac(Hrac):
    def __init__(self, barva_hrace, index_baru) -> None:
        super().__init__(barva_hrace, index_baru)

    def hrat_tah(self, legal_moves: dict) -> list:
        tah = check_input(input("Zadej tah: ").split(','))
        while True:
            for key, values in legal_moves.items():
                if tah[0] == key and tah[1] in values:
                    if tah[0] == "Bar":
                        return [self.bar.cislo_pole, tah[1]]
                    return tah 
            else:
                tah = check_input(input("Nelegální tah, zadejte tah znovu: ").split(','))


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
