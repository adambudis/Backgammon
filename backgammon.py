import random


def main():
    herni_deska = Herni_Deska()
    herni_deska.vytvor_kameny()
    print(herni_deska._herni_pole[1])
    #herni_deska._herni_pole[0].vloz_kamen(Kamen("cerna", 1))
    #print(herni_deska._herni_pole[0])


class Hra:
    pass


class Herni_Deska:
    def __init__(self) -> None:
        self._herni_pole = self.vytvor_herni_pole()

    @property
    def herni_pole(self) -> list:
        return self._herni_pole

    def vytvor_herni_pole(self) -> list:
        herni_pole = []
        for i in range(1, 24 + 1):
            herni_pole.append(Herni_Pole(i))
        return herni_pole

    def vytvor_kameny(self) -> list:
        new_cerny_kameny = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
        new_bily_kameny = [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

        for i in range(len(new_cerny_kameny)):
            for j in range(new_cerny_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Cerna", i))    

        for i in range(len(new_bily_kameny)):
            for j in range(new_bily_kameny[i]):
                    self._herni_pole[i].vloz_kamen(Kamen("Bila", i))   

    def __str__(self) -> str:
        return f"" 


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
        return f"Tento {self.barva_kamene} kamen je na pozici {self._historie[-1]}"


# modifikovany zasobnik
class Herni_Pole:
    def __init__(self, i: int, max_size=15) -> None:
        self._cislo_pole = i
        self._kameny = []
        # self._max_size = max_size

    def vloz_kamen(self, kamen: Kamen) -> None:
        self._kameny.append(kamen)

    def vytahni_kamen(self) -> Kamen:
        return self._kameny.pop()

    def koukni_na_kamen(self) -> Kamen:
        return self._kameny[-1]

    def je_prazdny(self) -> bool:
        return len(self._items) == 0

    def vrat_velikost(self) -> int:
        return len(self._items)

    @property
    def cislo_pole(self) -> int:
        return self._cislo_pole

    def __str__(self) -> str:
        return f"Herni pole cislo {self._cislo_pole} ma {len(self._kameny)} kamenu"


class Bar:
    pass


class Hrac:
    pass


class Konzolovy_Hrac(Hrac):
    pass


class AIHrac(Hrac):
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
