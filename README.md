# findBoroughToAdress
finds borough to adresses in csv-file using openplzapi

## input
csv-file in same path as python skript. 
the csv-file has to confirm to a strict format:
- adress (and housenumber) must be in column G with header 'strasse_nr'
- postal code and city must be in column H 
- every other column is ignored and will be copied into the output csv

## output
csv-file with additional column 'ortsteil' containing the borough 

## technical details
script uses the [openplzapi](https://www.openplzapi.org/de/germany/) 'Abfrage Straße'
if search with streetname, postal code and city was unsuccessful, the script does another FullTextSearch with the same informations

the streetname is readjusted before it can be used in the Api. The housenumber (and additions) is removed. The words 'Straße/Strasse' ist shortened to 'str'. This is necessary for the API to work properly. 

## general information
Inline comments are in german.  

## Planned Extensions
- choose csv file with GUI
- inout csv does not have to confirm to strict format
- general performance enhancments