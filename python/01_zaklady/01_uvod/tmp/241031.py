class Zvire:
    def __init__(self, jmeno, vek):
        self.jmeno = jmeno
        self.__vek = vek

    @property
    def vek(self):
        return self.__vek
    
    def vydej_zvuk(self):
        pass

    def spi(self):
        print(f"Zvíře {self.jmeno} spí...")

class Pes(Zvire):
    def __init__(self, jmeno, vek):
        super().__init__(jmeno, vek)

    def vydej_zvuk(self):
        self.aport()
        print("Haf!")
    
    def aport(self):
        print("Pes aportuje...")

class Kocka(Zvire):
    def __init__(self, jmeno, vek):
        super().__init__(jmeno, vek)
    
    def vydej_zvuk(self):
        print("Mňau!")

alik = Pes("Alík", 3)
mourek = Kocka("Mourek", 2)

print(alik.vek)
alik.vek = 8