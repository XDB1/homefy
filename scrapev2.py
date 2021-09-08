from pandas.core import series
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys

stadtliste = ['Münster','Düsseldorf','Köln','Bochum','Aachen']
trefferlistea = pd.Series([0,0,0,0,0],dtype=float)
trefferlistea.index = stadtliste
a=0

#info Erhalten

# Gastronomie

for i in stadtliste:
    urla = "https://www.gelbeseiten.de/Suche/restaurants/"+i
    pagea = requests.get(urla)
    soupa = BeautifulSoup(pagea.content, 'html.parser')
    resulta = soupa.find('span', {'id':"mod-TrefferlisteInfo"})

    # Ersgebnis zurechtschneiden
    resulta = str(resulta)
    resulta = resulta[:-7]
    resulta = resulta[32:]
    resulta = float(resulta)
    
    trefferlistea.iloc[a]=resulta
    a=a+1
    

df =pd.DataFrame(trefferlistea)
df.columns = ['Gastronomie']

# Sportvereine

trefferlisteb = pd.Series([0,0,0,0,0],dtype=float)
trefferlisteb.index = stadtliste
a=0
for i in stadtliste:
    urlb = "https://www.gelbeseiten.de/Suche/sportvereine/"+i
    pageb = requests.get(urlb)
    soupb = BeautifulSoup(pageb.content, 'html.parser')
    resultb = soupb.find('span', {'id':"mod-TrefferlisteInfo"})

    # Ersgebnis zurechtschneiden
    resultb = str(resultb)
    resultb = resultb[:-7]
    resultb = resultb[32:]
    resultb = float(resultb)
    trefferlisteb.iloc[a]=resultb
    a=a+1




df['Sportvereine']=trefferlisteb

# Schwimmbäder und Fitnesscenter

trefferlistec = pd.Series([0,0,0,0,0],dtype=float)
trefferlistec.index = stadtliste
a=0
for i in stadtliste:
    urlc1 = "https://www.gelbeseiten.de/Suche/Schwimmbäder/"+i
    pagec1 = requests.get(urlc1)
    soupc1 = BeautifulSoup(pagec1.content, 'html.parser')
    resultc1 = soupc1.find('span', {'id':"mod-TrefferlisteInfo"})

    # Ersgebnis zurechtschneiden
    resultc1 = str(resultc1)
    resultc1 = resultc1[:-7]
    resultc1 = resultc1[32:]
    resultc1 = float(resultc1)

    urlc2 = "https://www.gelbeseiten.de/Suche/Fitnesscenter/"+i
    pagec2 = requests.get(urlc2)
    soupc2 = BeautifulSoup(pagec2.content, 'html.parser')
    resultc2 = soupc2.find('span', {'id':"mod-TrefferlisteInfo"})

    # Ersgebnis zurechtschneiden
    resultc2 = str(resultc2)
    resultc2 = resultc2[:-7]
    resultc2 = resultc2[32:]
    resultc2 = float(resultc2)



    trefferlistec.iloc[a]=resultc1 + resultc2
    a=a+1




df['Schwimmbäder & Fitnesscenter']=trefferlistec

# Anteile Studenten
trefferlisted = pd.Series([0,0,0,0,0],dtype=float)
trefferlisted.index = stadtliste
a=0
for i in stadtliste:

    link = 'https://www.studis-online.de/Hochschulen/Hochschulstaedte/studentenstatistik.php'   
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find('ol',{'class': 'ston-spul ston-hashtag'})
    result_text = result.text.strip()
    name = i
    city = result_text.split(name,1)[1]
    city_number = city.split()
    x= city_number[3]
    x = x[1:]
    x = str(x[:-1])
    x = x.replace(',','.')
    x = float(x)
    trefferlisted.iloc[a]= x
    a=a+1
    

df['Anteil der Studenten %']=trefferlisted




# Wohnungsverfügbarkeit
cityid= ['91','30','73','12','1']
trefferlistee = pd.Series([0,0,0,0,0],dtype=float)
trefferlistee.index = stadtliste
a=0
for i in cityid:

    urle = "https://www.wg-gesucht.de/wg-zimmer-und-1-zimmer-wohnungen-in-Bochum.12.0+1.1.0.html?offer_filter=1&city_id="+ i +"&sort_column=0&noDeact=1&categories[]=0&categories[]=1&rent_types[]=0"
    pagee = requests.get(urle)
    soupee = BeautifulSoup(pagee.content, 'html.parser')
    resulte = soupee.find('h1', {'class':"headline headline-default"})

# Ersgebnis zurechtschneiden
    resulte = str(resulte)
    resulte = resulte.split()
    resulte = resulte[7]
    resulte = float(resulte)
    trefferlistee.iloc[a]=resulte
    a=a+1

df['Verfügbare Wohnungen']=trefferlistee


# Durchschnittsmiete

trefferlistef = pd.Series([0,0,0,0,0],dtype=float)
trefferlistef.index = stadtliste
a=0
staedtemiete= ['muenster','duesseldorf','koeln','bochum']
for i in staedtemiete:
    urlf = "https://www.immowelt.de/immobilienpreise/"+i+"/mietspiegel"
    pagef = requests.get(urlf)
    soupf = BeautifulSoup(pagef.content, 'html.parser')
    resultf = soupf.find('table', {'class':"table_01"})
    resultf = str(resultf)
    resultf = resultf.split()
    resultf = resultf[143]
    resultf = resultf[6:]
    resultf = resultf.replace(',','.')
    resultf = float(resultf)
    trefferlistef.iloc[a]=resultf
    a=a+1
    

trefferlistef.iloc[4]=float(8.70)


df['Miete pro qm']=trefferlistef








# Fortbewegung

vma = pd.Series([2,3,4,3,2], dtype = float)
vma.index = stadtliste


# Stadtgröße
stadtgrösse = pd.Series([303.28,217.41,405.02,145.66,160.85],dtype=float)
stadtgrösse.index = stadtliste

# Fachrichtungen

mint = pd.Series([4,5,2,4,10],dtype=float)
mint.index = stadtliste

mus = pd.Series([3,3,6,6,5], dtype = float)
mus.index = stadtliste

gwp = pd.Series([9,7,12,9,8], dtype = float)
gwp.index = stadtliste

dfvgl = df

df['Stadtgröße in qkm']=stadtgrösse

dfvgl = dfvgl.div(stadtgrösse, axis=0)

dfvgl['Anteil der Studenten %'] = df['Anteil der Studenten %']
dfvgl['Miete pro qm'] = df['Miete pro qm']

df['MINT Fachrichtung']=mint
df['Mensch Sozial Fachrichtung']=mus
df['Gesellschaft Wirtschaft Politik Fachrichtung']=gwp
df['Verkehrsmittelangebot']=vma

dfvgl['MINT Fachrichtung']=mint
dfvgl['Mensch Sozial Fachrichtung']=mus
dfvgl['Gesellschaft Wirtschaft Politik Fachrichtung']=gwp
dfvgl['Verkehrsmittelangebot']=vma
dfvgl['Stadtgröße in qkm']=stadtgrösse

dfrank = dfvgl

dfrank = dfrank.multiply(100000)
for col in dfrank:
    a=0
    b=0
    c=5
    while a < 5 :
        b=dfrank.max()[col]
        dfrank[col]=dfrank[col].replace(b,c)
        a= a + (dfrank[col]==c).sum()
        c=c- (dfrank[col]==c).sum()
        
stadtlistex = ['Münster','Düsseldorf','Köln','Bochum','Aachen','Perfekte Stadt']
pcity= pd.DataFrame([[5,5,5,5,5,5,5,5,5,5,5]],columns=pd.Series(dfrank.columns))        
dfrank = dfrank.append(pcity, ignore_index=False)
dfrank.index = stadtlistex

# Data ranked based on extracted values from webpages
dfrank.to_csv('score_new.csv')
# Data feature (restaurants, sport centers, appartments etc) values
df.to_csv('original_new.csv')
dfverr = dfrank



