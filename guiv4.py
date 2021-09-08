from tkinter import *
import pandas as pd


def main():
    root = Tk()
    populate_text(root)

    # Werte der 11 Radiobuttons
    radio_vars = [DoubleVar(root) for i in range(11)]
    values = {"irrelevant": 0,
              "wenig relevant": 0.5,
              "neutral": 1,
              "etwas relevant": 1.5,
              "sehr relevant": 2}
    # Populate radio buttons in the grid
    for i in range(len(radio_vars)):
        j = 1
        for (text, value) in values.items():
            Radiobutton(root, text=text, variable=radio_vars[i], value=value).grid(row=i + 10, column=j)
            radio_vars[i].set(value=1)
            j = j + 1

    # Knopf zum Bestätigen der Präferenzen
    Button(root, text="Bestätigen", command=lambda: submit(radio_vars)).grid(row=21, column=0)

    # Knopf zum Zurücksetzen der Präferenzen
    Button(root, text="Zurücksetzen", command=lambda: reset(radio_vars)).grid(row=21, column=1)

    root.mainloop()


def populate_text(root):
    root.title("homefy")
    # Einführungstext
    myLabel1 = Label(root, text="Willkommen zu homefy")
    myLabel1.config(font=("Courier", 25))
    myLabel1.grid(row=0, column=0)
    myLabel2 = Label(root,
                     text="Damit wir dir helfen können, die zu dir am besten passende Stadt zu finden, \nmüssen wir wissen wie wichtig dir bestimmte Aspekte sind. Im Folgenden \nkannst du deine Präferenzen zu 11 verschiedenen Kriterien abgeben.\nBitte stelle sicher, dass du alle Fragen beantwortest\nund bestätige dann unten deine Auswahl.")
    myLabel2.grid(row=1, column=0)
    myLabel2 = Label(root, text=" ")
    myLabel2.grid(row=2, column=0)

    questions = ['Wie wichtig sind dir viele Gastronomien?', 'Wie wichtig sind dir viele Sportvereine?',
                 'Wie wichtig sind dir viele Schwimmbäder und Fitnesscenter?',
                 'Wie wichtig ist dir ein hoher Anteil der Studenten?',
                 'Wie wichtig ist dir die Wohnungsverfügbarkeit ?', 'Wie wichtig ist dir der Mietpreis?',
                 'Wie wichtig ist dir, dass die Stadt groß ist?', 'Relevanz des Angebots von MINT Fächern?',
                 'Relevanz des Angebots von Mensch und Sozial Fächern',
                 'Relevanz des Angebots von Gesellschaft, Wirtschaft oder Politik Fächern',
                 'Wie wichtig ist dir das Verkehrsmittelangebot?']
    for i in range(len(questions)):
        Label(root, text=str(questions[i])).grid(row=10 + i, column=0)


# Code für die Ergebnisausgabe auf der 2. Seite
def submit(radio_values):
    top = Toplevel()
    top.title("Ergebnis")

    values = [var.get() for var in radio_values]
    best_city, ranked_cities = calculate(values)
    best_city = best_city.to_list()
    #print(ranked_cities)

    Label(top, text="Die Stadt, welche deinen \nPräferenzen am meisten \nentspricht ist " + str(best_city[0]),
          font=("Courier", 25)).grid(row=0, column=3)

    stat_labels = ['Anzahl Gastronomien:',
                   'Anzahl Sportvereine:',
                   'Anzahl Schwimmbäder & Fitnesscenter:',
                   'Anteil der Studenten in %:',
                   'Verfügbare Wohnungen:',
                   'Miete pro qm in €:',
                   'Stadtgröße in qkm:',
                   'Anzahl MINT Fachrichtungen:',
                   'Anzahl Mensch Sozial Fachrichtungen:',
                   'Anzahl Ges.-Wirt.-Poli. Fachrichtungen:',
                   'Arten von Verkehrsmitteln:']

    for i in range(len(stat_labels)):
        # text = str(city_stats[i]) + "       " + str(scrape_values[i+1])
        Label(top, text=str(stat_labels[i])).grid(row=3 + i, column=3)
        Label(top, text=str(int(best_city[i + 1]))).grid(row=3 + i, column=4)

    # Second best city
    Label(top, text="\nDie zweit beste Stadt für dich wäre: " + str(ranked_cities[1][0]), font="10").grid(row=14, column=3)

    #Label(top, text="Ranking order").grid(row=14, column=3)
    #ranked_lables = [str(city[0]) for city in ranked_cities]
    #j = 0
    #for i in range(len(ranked_lables)):
    #    Label(top, text="Rank "+str(i+1), font="bold").grid(row=j+15, column=3)
    #    Label(top, text=str(ranked_lables[i])).grid(row=j+16, column=3)
    #    j = j + 2


# Angabe zum zurücksetzen der Werte
def reset(radio_vars):
    for i in radio_vars:
        i.set(value=None)


def calculate(user_input):
    dfverr = pd.read_csv('score.csv')
    df = pd.read_csv('original.csv')
    testeingaben = pd.Series(user_input, dtype=float)
    testeingaben.index = ['Gastronomie', 'Sportvereine', 'Schwimmbäder & Fitnesscenter', 'Anteil der Studenten %',
                          'Verfügbare Wohnungen', 'Miete pro qm', 'Stadtgröße in qkm', 'MINT Fachrichtung',
                          'Mensch Sozial Fachrichtung', 'Gesellschaft Wirtschaft Politik Fachrichtung',
                          'Verkehrsmittelangebot']
    dfverr = dfverr.mul(testeingaben)
    punkte = dfverr.iloc[0:6].sum(axis=1)
    musterstadtpunkte = punkte.max()

    punkteb = punkte.replace(punkte.max(), 0)
    bestestadt = punkteb.idxmax()

    bestestadtpunkte = punkteb.max()

    punkteb = punkteb.replace(punkteb.max(), 0)
    nbestestadt = punkteb.idxmax()

    # third
    punkteb = punkteb.replace(punkteb.max(), 0)
    third = punkteb.idxmax()

    # fourth
    punkteb = punkteb.replace(punkteb.max(), 0)
    fourth = punkteb.idxmax()

    # fifth
    punkteb = punkteb.replace(punkteb.max(), 0)
    fifth = punkteb.idxmax()

    nbestestadtpunkte = punkteb.max()
    #bestestadtpro = bestestadtpunkte / musterstadtpunkte * 100
    Bestestadtspecs = df.loc[bestestadt, :]
    nBestestadtspecs = df.loc[nbestestadt, :]
    third_best = df.loc[third, :]
    fourth_best = df.loc[fourth, :]
    fifth_best = df.loc[fifth, :]
    gastro = Bestestadtspecs[0]
    # First and second best cities
    cities = [Bestestadtspecs, nBestestadtspecs]
    ranked_cities = [city.to_list() for city in cities]
    # punkte.to_csv('tmp1.csv')
    # print(dfverr)
    # print(punkte)
    # print(musterstadtpunkte)
    # print(bestestadt)
    # print(bestestadtpunkte)
    # print(nbestestadt)
    # print(nbestestadtpunkte)
    # print(bestestadtpro)
    # Bestestadtspecs.to_csv('tmp.csv')
    # print(Bestestadtspecs)

    # output = str(str(bestestadt) + str(bestestadtpunkte) + str(nbestestadt))
    return Bestestadtspecs, ranked_cities


if __name__ == '__main__':
    main()
