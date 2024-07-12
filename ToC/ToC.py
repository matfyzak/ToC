import random

VYCHOZI_CISTOTA_VODY = 100
EFEKT_CISTENI = 3
MAX_ZISK_Z_RYBARENI = 6
MAX_ZISK_Z_MAGICKEHO_RYBARENI = 20
POSKOZENI_MAGICKYM_RYBARENIM = 5

class Vizualizace:
    def generate_html(cistota_vody, cislo_kola):
        fish_count = cistota_vody
        fish_html = ""
        for _ in range(fish_count*2):
            x = random.randint(3, 90) 
            y = random.randint(20, 85) # nechci překrýt nápis
            mirror = random.choice([True, False]) # některé ryby chci obrátit
            transform = "scaleX(-1)" if mirror else "none"

            if cistota_vody < VYCHOZI_CISTOTA_VODY // 2:
                if random.random() / 2 > cistota_vody / VYCHOZI_CISTOTA_VODY:
                    fish_html += f'<img src="mutant.png" class="fish" style="position:absolute; left:{x}%; top:{y}%; width:120px; height:120px; z-index: 1; transform:{transform};">\n' # z-index posouvá monstra do popředí, šlo by dělat pomocí CSS
                else:
                    fish_html += f'<img src="ryba.png" class="fish" style="position:absolute; left:{x}%; top:{y}%; width:70px; height:70px; transform:{transform};">\n'
            else:
                 fish_html += f'<img src="ryba.png" class="fish" style="position:absolute; left:{x}%; top:{y}%; width:70px; height:70px; transform:{transform};">\n'

        surface_html = '<img src="surface.png" class="water-level" style="position: absolute; top: 7%; left: 0; width: 100%; height: auto; z-index: -1;">'

        html_content = f"""
        <html style="max-width: 100%; max-height: 100%; overflow-x: hidden;">

        <head>
            <title>Vizualizace Čistoty Vody</title>
            <meta http-equiv="refresh" content="10"> 

        </head>
        <body style="position:relative; width:100vw; height:100vh; margin:30; padding:20;">
            <h1>Čistota vody: {cistota_vody}</h1>
            <h1>Číslo kola: {cislo_kola}</h1>
            {surface_html}
            {fish_html}              
        </body>
        </html>
        """

        with open("index.html", "w") as file:
            file.write(html_content)

class Hra:
    def __init__(self, pocet_tymu):
        self.cistota_vody = VYCHOZI_CISTOTA_VODY
        self.skore = {chr(65+i): 0 for i in range(pocet_tymu)}
        self.akce = {chr(65+i): None for i in range(pocet_tymu)}
        self.poradi = sorted(self.skore.keys())
        self.index_aktualniho_tymu = 0  
        self.cislo_kola = 1

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
        print(f"\nVyhodnocení kola {self.cislo_kola}")

        for tym, akce in self.akce.items():
            if akce is None:
                raise TypeError("Každý tým muí zvolit před vyhodnocením kola nějakou akci")

        vychozi_cistota_vody = self.cistota_vody # počítá se s čistotou vody na začátku kola

        for tym, akce in self.akce.items(): # prvně se vyhodnotí klasické rybaření, to proběhne v každém případě
            if akce[0] == 'rybaření':
                body = random.randint(1, MAX_ZISK_Z_RYBARENI) * (vychozi_cistota_vody / VYCHOZI_CISTOTA_VODY)
                self.skore[tym] += body
                print(f"Tým {tym} provedl rybolov a získal {body:.2f} bodů.")

        for tym, akce in self.akce.items(): # akce už jsou dané, jinak by se nevyhodnocovalo kolo
            if akce[0] == 'špionáž':
                cil = akce[1]
                posledni_akce = self.akce[cil][0] # jinak nehezký formát
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
                    body = random.randint(1, MAX_ZISK_Z_MAGICKEHO_RYBARENI) * (vychozi_cistota_vody / VYCHOZI_CISTOTA_VODY)
                    self.skore[tym] += body
                    self.cistota_vody = max(0, self.cistota_vody - POSKOZENI_MAGICKYM_RYBARENIM)
                    print(f"Tým {tym} provedl úspěšně rybaření pomocí magie a získal {body:.2f} bodů.")
                else:
                    print(f"Tým {tym} provedl neúspěšně rybařené pomocí magie.")

        for tym, akce in self.akce.items(): # čištění až úplně nakonec, aby se vyčistilo i to co se zašpinilo v tomto kole
            if akce[0] == 'čištění':
                self.cistota_vody = min(VYCHOZI_CISTOTA_VODY, self.cistota_vody + EFEKT_CISTENI)
                print(f"Tým {tym} provedl čištění.")

        self.akce = {chr(65+i): None for i in range(len(self.skore))} # vymažeme akce, už není potřeba si je pamatovat

        Vizualizace.generate_html(self.cistota_vody, self.cislo_kola)
        self.zobraz_skore()
        self.cislo_kola += 1

    def zobraz_skore(self): # skóre by mělo zůstat tajné! - zobrazí se někam jen čistota vody!
        print("\nPrůběžné skóre:")
        for tym, skore in self.skore.items():
            print(f"Tým {tym}: {skore:.2f} bodů")
        print(f"Čistota vody: {self.cistota_vody}")     


def interaktivni_hra():
    print("Tohle okno účastníci nesmí vidět!! - říká se jim jen výsledek špionáže.")

    pocet_hracu = int(input("Zadejte počet hráčů:"))
    hra = Hra(pocet_hracu)



    while True:
        aktualni_tym = hra.poradi[hra.index_aktualniho_tymu]
        print(f"\nNa řadě je tým {aktualni_tym}.")
        print("Vyberte akci:")
        print("1. Rybolov")
        print("2. Rybolov pomocí magie")
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

# FIXME nějak implementovat staty ještě?
# FIXME odstranit scrollování stránky
# FIXME nějaká hezčí grafika - kouzelník, rybář, rybník atd.