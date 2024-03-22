
[[#Grundkonzepte Data Wrangling|Grundkonzepte Data Wrangling]]
- [[#six steps of data wrangling|six steps of data wrangling]]
- [[#Data Fit|Data Fit]]
	- [[#Data Fit#1. data validity|1. data validity]]
	- [[#Data Fit#2. data reliability|2. data reliability]]
	- [[#Data Fit#3. representatives|3. representatives]]
- [[#Data Integrity|Data Integrity]]
	- [[#Data Integrity#Importance of integrity characteristics|Importance of integrity characteristics]]
- [[#difference between data fit and data integrity?|difference between data fit and data integrity?]]


[[#Datenqualität|Datenqualität]]
- [[#file based and feed based data|file based and feed based data]]
- [[#structured data|structured data]]
- [[#denominator problem|denominator problem]]
- [[#fingerprint algorithm|fingerprint algorithm]]
- [[#Best practice to correct spelling inconsistencies|Best practice to correct spelling inconsistencies]]
- [[#Describe missing value imputation|Describe missing value imputation]]


# Grundkonzepte Data Wrangling
## six steps of data wrangling  
1. Locating or collecting data  
2. Reviewing the data  
3. "Cleaning": standardizing, transforming, augmenting the data  
4. Analyzing the data  
5. Visualizing the data  
6. Communicating the data  

  
## Data Fit  
How useful a dataset is for a particular purpose

### 1. data validity
data validity: the extent to which something measures what it is supposed to  
1. construct validity: extent to which your data measurements effectively capture the construct  
2. content validity: how complete your data is for given prox measurement  

### 2. data reliability
It describes the accuracy and stability.  
-> assesses if the same measurement will give the same result s if the same measurement will give the same result  

### 3. representatives
How does the sample represent about the group we want to know about about.


## Data Integrity 
Data integrity refers to the **accuracy, consistency, and reliability** of data throughout its entire lifecycle.  
### Importance of integrity characteristics  

1. **Achievable**: 
   - Consistent: gaps? are the attribute types consistent? (ex strings with same meaning)
   - Clear:  all abbreviations clear? understandable?
   - Dimensionally structured: efficient queries possible?

2. **Important**: 
   - Timely: how old is too old?
   - Complete: if missing data? do we need those data?
   - High volume: genug Daten für eine Aussage
   - Multivariate: has it more attributes to generate more meaning?
   - Atomic: jeder Datenpunkt steht für sich

3. **Necessary, but not sufficient**: 
	 * Of known provenance: how much do we know about the source?
	-  well-annotated : metadata/notes?



## difference between data fit and data integrity?
Data fit is whether you have the right data for answering your data wrangling question.  
Data integrity is whether the data you have can support the analyses you'll need to perform in order to answer that question.  

----


# Datenqualität  
##  file based and feed based data
- **file based**: on the data server the new data overwrites the old data file
- **feed based**: the new data is appended to the old data file

## structured data
Structured data is any type of data that has been organized and classified in some way, into some version of records and fields

file based: rows and columns
feed based: lists of objects or dictionaries

## denominator problem 
other names: benchmarking problem, baseline problem
The denominator problem is the problem of trying to draw meaning from data when you lack sufficient comparative information to put it into context. (comparison data you really need was never collected)
- solution: build own data archive

## fingerprint algorithm 
1. removes leading and trailing whitespace  
2. changes all characters to their lowercase representation  
3. removes all punctuation and control characters  
4. normalizes extended western characters to their ASCII representation  
5. splits the string into whitespace-separated tokens  
6. sorts the tokens and removes duplicates  
7. joins the tokens back together   

# types of bias 
1. Pre-existing bias: bias from society based on a belief system  
2. Technical bias: due to technical system  
3. Emergent bias: from use of technical system  
  
## Best practice to correct spelling inconsistencies

- add additional column for using the fingerprint algorithm


## Describe missing value imputation
- korrekte Werte ermitteln  
- Zeilen mit fehlenden Werten löschen / Spalte mit fehlenden Werten löschen  
- Neuen Werte einsetzen: Neue Kategorie  
- Mode Imputation: fehlende Werte mit dem häufigsten Werte ersetzen  
- Mean Imputation: fehlenden Werte werden durch den Mittelwert ersetzt  
- Median Impuation - Imputation value: mit 0 oder anderem konstantem Wert  
- modell-basierte Imputation: ML Modell Zusätzlich kann ein weiteres Feature erstellt werden, um zu kennzeichnen, ob eine Imputation vorgenommen wurde



Das Ersetzen von fehlenden Werten wird als *(Missing Value) Imputation* bezeichnet. Hierfür gibt es verschiedene Strategien:
- Korrekten Wert ermitteln: Im besten Fall kann der korrekte Wert ermittelt werden, bspw. durch Rücksprache mit (Fach-)Expert\*innen. Dies ist jedoch nur selten der Fall und häufig mit großem Aufwand verbunden.
- Zeilen mit fehlenden Werten löschen: Fehlen wenige, einzelne Werte, kann es u.U. sinnvoll sein, die entsprechenden Zeilen zu löschen. Hierbei muss jedoch darauf geachtet werden, dass nicht zu viele Informationen verloren gehen.
- Spalte mit fehlenden Werten löschen: Fehlen in einer Spalte so viele Werte, dass diese keine Aussagekraft mehr hat, kann es sinnvoll sein, die gesamte Spalte zu entfernen.
- Neuen Wert einsetzen:
    - Neue Kategorie: Bei nominalen Werten kann eine neue Kategorie (z.B. "Unbekannt") eingeführt werden.
    - Mode Imputation: Die fehlenden Werte werden durch den am häufigst vorkommenden Wert ersetzt.
    - Mean Imputation: Die fehlenden Werte werden durch den Mittelwert ersetzt.
    - Median Imputation: Die fehlenden Werte werden durch den Median ersetzt.
    - Mode, Mean und Median Imputation können auch basierend auf den Werten einer anderen Spalte vorgenommen werden (in unserem Fall z.B. für zufriedene und unzufriedene Angestellte getrennt).
    - Imputation mit 0 oder einem anderen konstanten Wert: Die fehlenden Werte werden durch eine 0 oder eine andere, je nach Anwendungsfall passende, Konstante ersetzt.
    - Modell-basierte Imputation: Es wird ein Machine-Learning-Modell trainiert, das die fehlenden Werte vorhersagt.
    - Zusätzlich zu den genannten Strategien ist es möglich, ein neues Feature zu erstellen, das kennzeichnet, ob eine Imputation vorgenommen wurde (=1) oder nicht (=0).