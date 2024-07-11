import random

class Hra:
    def __init__(self, pocet_tymu):
        self.cistota_vody = 100
        self.skore = {chr(65+i): 0 for i in range(pocet_tymu)}
        self.akce = {chr(65+i): None for i in range(pocet_tymu)}
        self.poradi = sorted(self.skore.keys())
        self.index_aktualniho_tymu = 0


    def dalsi_tym(self):
        self.index_aktualniho_tymu = (self.index_aktualniho_tymu + 1) % len(self.skore)
        if self.index_aktualniho_tymu == 0:
            self.vyhodnotit_kolo()

    def rybolov(self, tym):
        self.akce[tym] = ('rybaření',)
        print(f"Tým {tym} plánuje rybařit.")
        self.dalsi_tym()

    def rybareni_pomoci_magie(self, tym):
        self.akce[tym] = ('rybaření pomocí magie',)
        print(f"Tým {tym} plánuje rybařit pomocí magie.")
        self.dalsi_tym()

    def cisteni(self, tym):
        self.akce[tym] = ('čištění',)
        print(f"Tým {tym} plánuje čištění.")
        self.dalsi_tym()

    def spionaz(self, tym, cil):
        self.akce[tym] = ('špionáž', cil)
        print(f"Tým {tym} plánuje špehovat tým {cil}.")
        self.dalsi_tym()

    def udani(self, tym, cil):
        self.akce[tym] = ('udání', cil)
        print(f"Tým {tym} plánuje udat tým {cil}.")
        self.dalsi_tym()

    def vyhodnotit_kolo(self):
        print("Vyhodnocení kola...")

        for tym, akce in self.akce.items():
            if akce is None:
                raise TypeError("Každý tým muí zvolit před vyhodnocením kola nějakou akci")

        vychozi_cistota_vody = self.cistota_vody # počítá se s čistotou vody na začátku kola

        for tym, akce in self.akce.items(): # prvně se vyhodnotí klasické rybaření, to proběhne v každém případě
            if akce[0] == 'rybaření':
                body = random.randint(1, 6) * (vychozi_cistota_vody / 100)
                self.skore[tym] += body
                print(f"Tým {tym} provedl rybolov a získal {body:.2f} bodů.")

        for tym, akce in self.akce.items(): # akce už jsou dané, jinak by se nevyhodnocovalo kolo
            if akce[0] == 'špionáž':
                cil = akce[1]
                posledni_akce = self.akce[cil]
                print(f"Tým {tym} špehoval tým {cil} a zjistil, že tým {cil} provedl akci: {posledni_akce}.")

        udane_tymy = [] 

        for tym, akce in self.akce.items(): # akce už jsou dané, jinak by se nevyhodnocovalo kolo
            if akce[0] == 'udání':
                cil = akce[1]
                udane_tymy.append(cil)
                print(f"Tým {tym} udal tým {cil}.")

        for tym, akce in self.akce.items():
            if akce[0] == 'rybaření pomocí magie':
                if tym not in udane_tymy: # proběhne normálně jako rybaření, akorát výhodnější
                    body = random.randint(1, 20) * (vychozi_cistota_vody / 100)
                    self.skore[tym] += body
                    self.cistota_vody = max(0, self.cistota_vody - 5)
                    print(f"Tým {tym} provedl úspěšně rybaření pomocí magie a získal {body:.2f} bodů.")
                else:
                    print(f"Tým {tym} provedl neúspěšně rybařené pomocí magie.")

        for tym, akce in self.akce.items(): # čištění až úplně nakonec, aby se vyčistilo i to co se zašpinilo v tomto kole
            if akce[0] == 'čištění':
                self.cistota_vody = min(100, self.cistota_vody + 3)
                print(f"Tým {tym} provedl čištění.")

        self.akce = {chr(65+i): None for i in range(len(self.skore))} # vymažeme akce, už není potřeba si je pamatovat

        self.zobraz_skore()

    def zobraz_skore(self): # skóre by mělo zůstat tajné! - zobrazí se někam jen čistota vody!
        print("Průběžné skóre:")
        for tym, skore in self.skore.items():
            print(f"Tým {tym}: {skore:.2f} bodů")
        print(f"Čistota vody: {self.cistota_vody}")     


def interaktivni_hra():
    pocet_hracu = int(input("Zadejte počet hráčů:"))
    hra = Hra(pocet_hracu)

    while True:
        aktualni_tym = hra.poradi[hra.index_aktualniho_tymu]
        print(f"\nNa řadě je tým {aktualni_tym}.")
        print("Vyberte akci:")
        print("1. Rybolov")
        print("2. Průmyslový rybolov")
        print("3. Čištění")
        print("4. Špionáž")
        print("5. Udání")
        
        akce = input("Zadejte číslo akce: ")
        

        if akce == '1':
            hra.rybolov(aktualni_tym)
        elif akce == '2':
            hra.rybareni_pomoci_magie(aktualni_tym)
        elif akce == '3':
            hra.cisteni(aktualni_tym)
        elif akce == '4':
            while True:
                cil = input("Zadejte tým, který chcete špehovat: ")
                if cil in hra.skore and aktualni_tym != cil: # nelze špehovat sebe sama
                    break
                else:
                    print("Neplatný tým. Zadejte platný tým.")
            hra.spionaz(aktualni_tym, cil)
        elif akce == '5':
            while True:
                cil = input("Zadejte tým, který chcete udat: ")
                if cil in hra.skore:
                    break
                else:
                    print("Neplatný tým. Zadejte platný tým.")
            hra.udani(aktualni_tym, cil)
        else:
            print("Neplatná akce. Zkuste to znovu.")
            continue



# spustit interaktivní hru
interaktivni_hra()