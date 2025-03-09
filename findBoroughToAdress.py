import requests
import urllib.parse
import re
import json
import csv
import glob

#Funktion um Straßennummer abzuschneiden und aus Straße/Strasse Str zu machen
def readjust_streetname(inputStraßeHausnummer):
    
    #regex: eine mind. einstellige Zahl die von einem Buchstaben zwischen a-z gefolgt werden kann
    straßenname = inputStraßeHausnummer.replace('/','')
    straßenname = re.sub(r'([0-9]+[(a-z)|(A-Z)]{0,1})', '', straßenname).strip()
    #regex: substring traße oder trasse
    straßenname = re.sub(r'(tra(ß|ss)e)', 'tr', straßenname).strip()
    #regex: substring " -"
    straßenname = straßenname.replace('-',' ').strip()
    return straßenname



#Funktion um den Stadtteil zu einer Straße, Plz und Ort zu finden
def find_borough(inputStraßeHausnummer,inputPlzOrt):
#Hinweis: Die Straßennamen dürfen nur str heißen
    straße = readjust_streetname(inputStraßeHausnummer)
    plz = inputPlzOrt.split()[0]
    ort = inputPlzOrt.split()[1]

    params = {'name': straße, 'postalCode': plz, 'locality': ort}
    url = "https://openplzapi.org/de/Streets?" + urllib.parse.urlencode(params)


    response = requests.get(url).json()

    #Manchmal findet die direkt suche nix, weil der Straßenname wirklich doof aufgebaut ist. Dann wird nochmal die Volltextsuche aufgerufen.
    if len(response) == 0:
        search_term = straße.replace(' ','%20') + '%20' + ort
        url = "https://openplzapi.org/de/FullTextSearch?searchTerm=" + search_term
        response = requests.get(url).json()

    for item in response:
       return item.get('borough')
    

#main-function: liest daten aus csv, sucht Ortsteil und schreibt Ergebnis in eine eigene Liste
def main(input_datei, output_datei): 
    with open(input_datei, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        data_list = []
        for row in spamreader:
            if row[6] == 'strasse_nr':
               header = row
            else:
                row_with_borough = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],find_borough(row[6],row[7])]
                data_list.append(row_with_borough)

    with open(output_datei, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(data_list)


#Skript wird ausgeführt
mitgliederliste = glob.glob('*.csv')
for item in mitgliederliste:
    print(item + ' wird eingelesen und verarbeitet!')
    outputdatei = item.replace('.csv','_mitOrtsteil.csv')
    main(item, outputdatei)
print('FERTIG!')
