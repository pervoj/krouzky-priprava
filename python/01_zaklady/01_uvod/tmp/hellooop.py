int()
str()

# class Pes:
#     def __init__(self, jmeno):
#         self.name = jmeno
    
#     def zvuk(self):
#         print(f"{self.jmeno} štěká")

class Zvire:
    def __init__(self, jmeno):
        self.jmeno = jmeno
    
    def zvuk(self):
        print(f"{self.jmeno} vydává zvuk")

class Pes(Zvire):
    def __init__(self, jmeno):
        super().__init__(jmeno)
    
    def zvuk(self):
        print(f"{self.jmeno} štěká")

class Kocka(Zvire):
    def __init__(self, jmeno):
        super().__init__(jmeno)
    
    def zvuk(self):
        print(f"{self.jmeno} mňouká")

alik = Pes("Alík")
alik.zvuk()

micka = Kocka("Micka")
micka.zvuk()