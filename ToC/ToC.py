import random

class Hra:
    def __init__(self, pocet_hracu):
        self.cistota_vody = 100
        self.skore = {chr(65+i): 0 for i in range(pocet_hracu)}
        self.akcni_log = {chr(65+i): [] for i in range(pocet_hracu)}
        self.akce_v_kole = {chr(65+i): None for i in range(pocet_hracu)}
        self.poradi_tymu = sorted(self.skore.keys())
        self.aktualni_tym_index = 0


    def dalsi_tym(self):
        self.aktualni_tym_index = (self.aktualni_tym_index + 1) % len(self.skore)
        if self.aktualni_tym_index == 0:
            self.vyhodnotit_kolo()

    def rybolov(self, tym):
        self.akce_v_kole[tym] = ('rybolov',)
        print(f"Tým {tym} plánuje rybolov.")
        self.dalsi_tym()

    def prumyslovy_rybolov(self, tym):
        self.akce_v_kole[tym] = ('průmyslový rybolov',)
        print(f"Tým {tym} plánuje průmyslový rybolov.")
        self.dalsi_tym()

    def cisteni(self, tym):
        self.akce_v_kole[tym] = ('čištění',)
        print(f"Tým {tym} plánuje čištění.")
        self.dalsi_tym()

    def spionaz(self, tym, cil):
        self.akce_v_kole[tym] = ('špionáž', cil)
        print(f"Tým {tym} plánuje špehovat tým {cil}.")
        self.dalsi_tym()

    def udani(self, tym, cil):
        self.akce_v_kole[tym] = ('udání', cil)
        print(f"Tým {tym} plánuje udat tým {cil}.")
        self.dalsi_tym()

    def vyhodnotit_kolo(self):
        print()
        print("Vyhodnocení kola...")

        vychozi_cistota_vody = self.cistota_vody

        for tym, akce in self.akce_v_kole.items():
            if akce[0] == 'rybolov':
                body = random.randint(1, 6) * (vychozi_cistota_vody / 100)
                self.skore[tym] += body
                self.akcni_log[tym].append('rybolov')
                print(f"Tým {tym} provedl rybolov a získal {body:.2f} bodů.")

        for tym, akce in self.akce_v_kole.items():
            if akce[0] == 'špionáž':
                cil = akce[1]
                posledni_akce = self.akce_v_kole[cil]
                self.akcni_log[tym].append(f"špionáž týmu {cil}")
                print(f"Tým {tym} špehoval tým {cil} a zjistil, že tým {cil} provedl akci: {posledni_akce}.")

        udane_tymy = []

        for tym, akce in self.akce_v_kole.items():
            if akce[0] == 'udání':
                cil = akce[1]
                self.akcni_log[tym].append(f"udání týmu {cil}")
                udane_tymy.append(cil)
                print(f"Tým {tym} udal tým {cil}.")

        for tym, akce in self.akce_v_kole.items():
            if akce[0] == 'průmyslový rybolov':
                if tym not in udane_tymy:
                    body = random.randint(1, 20) * (vychozi_cistota_vody / 100)
                    self.skore[tym] += body
                    self.cistota_vody = max(0, self.cistota_vody - 5)
                    self.akcni_log[tym].append('úspěšný průmyslový rybolov')
                    print(f"Tým {tym} provedl úspěšně průmyslový rybolov a získal {body:.2f} bodů.")
                else:
                    self.akcni_log[tym].append('neúspěšný průmyslový rybolov')
                    print(f"Tým {tym} provedl neúspěšně průmyslový rybolov.")

        for tym, akce in self.akce_v_kole.items():
            if akce[0] == 'čištění':
                self.akcni_log[tym].append('čištění')
                self.cistota_vody = min(100, self.cistota_vody + 3)
                print(f"Tým {tym} provedl čištění.")

        self.akce_v_kole = {chr(65+i): None for i in range(len(self.skore))}
        self.zobraz_skore()


        self.root = tk.Tk()
        self.root.title("Hra o čistotu vody")

        # Proměnné pro zobrazení čistoty vody a ryb v jezeře
        self.cistota_vody_label = tk.Label(self.root, text="Čistota vody: 100")
        self.cistota_vody_label.pack()

        self.jezero_canvas = tk.Canvas(self.root, width=400, height=200, bg="lightblue")
        self.jezero_canvas.pack()

        self.aktualizovat_cistotu_vody(self.cistota_vody)
        self.aktualizovat_ilustraci_jezera()

    def zobraz_skore(self):
        print("Průběžné skóre:")
        for tym, skore in self.skore.items():
            print(f"Tým {tym}: {skore:.2f} bodů")
        print(f"Čistota vody: {self.cistota_vody}")

    def aktualizovat_cistotu_vody(self, cistota_vody):
        self.cistota_vody_label.config(text=f"Čistota vody: {cistota_vody}")

    def aktualizovat_ilustraci_jezera(self, pocet_ryb):
        self.jezero_canvas.delete("ryba")  # Vymažeme předchozí ryby
        for i in range(pocet_ryb):
            x = random.randint(50, 350)
            y = random.randint(50, 150)
            self.jezero_canvas.create_oval(x-10, y-10, x+10, y+10, fill="red", tags="ryba")

    def spustit_hru(self):
        self.root.mainloop()

def interaktivni_hra():
    pocet_hracu = int(input("Zadejte počet hráčů:"))
    hra = Hra(pocet_hracu)
    hra.spustit_hru()

    while True:
        aktualni_tym = hra.poradi_tymu[hra.aktualni_tym_index]
        print(f"\nJe řada týmu {aktualni_tym}.")
        print("Vyberte akci:")
        print("1. Rybolov")
        print("2. Průmyslový rybolov")
        print("3. Čištění")
        print("4. Špionáž")
        print("5. Udání")
        
        akce = input("Zadejte číslo akce: ")
        
        try:
            if akce == '1':
                hra.rybolov(aktualni_tym)
            elif akce == '2':
                hra.prumyslovy_rybolov(aktualni_tym)
            elif akce == '3':
                hra.cisteni(aktualni_tym)
            elif akce == '4':
                while True:
                    cil = input("Zadejte tým, který chcete špehovat: ")
                    if cil in hra.skore:
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
        except ValueError as e:
            print(e)
            continue


# Spustit interaktivní hru
interaktivni_hra()