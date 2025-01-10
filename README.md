# Afwerken, testen en eindreflectie

## Doel
De opdracht voor deze laatste weken was om de Trojan af te werken, te testen in een veilige en gecontroleerde omgeving.

---

## Bevindingen

### Configuratie
Het configuratiebestand (`config.json`) is modulair opgezet en maakt het mogelijk om modules dynamisch te activeren of configureren zonder wijzigingen aan de kerncode. Belangrijkste parameters:
- **Poll Interval**: Modules worden iedere 60 seconden uitgevoerd.
- **Modules**:
  - **Portscanner**: Scant IP's en poorten.
  - **System Enumeration**: Verzamelt systeeminformatie.
  - **Backdoor**: Reverse shell-functionaliteit.

### Code
#### Core (`main.py`)
- **Functionaliteit**: 
  - Dynamisch laden van modules.
  - Opslaan van resultaten.
  - Bevat integratie met een private GitHub-repository voor configuratiebeheer.

#### Modules

1. **Backdoor**
   - **Reverse Shell**: Verbindt naar een opgegeven IP-adres en poort.
   - **Functie**: Ontvangt en verwerkt commando's van de aanvallende machine.

2. **Portscanner**
   - **Scan Port**: Controleert of een specifieke poort op een doel-IP open of gesloten is.
   - **Scan Target**: Scant specifieke poorten of een reeks poorten op een opgegeven IP-adres.
   - **Scan Common Ports**: Controleert veelgebruikte poorten zoals `80`, `443`, en `22` op een doelwit.
   - **Discover IPs**: Zoekt actieve apparaten binnen een specifiek subnet.
   - **Detect OS**: Identificeert het besturingssysteem van een doel-IP via TTL-waarden.
   - **Get IP Details**: Haalt hostnaam en DNS-gegevens op voor een specifiek IP.
   - **Functie**: Gebruik van threading voor snelheid en efficiëntie bij het scannen van netwerken.

3. **System Enumeration**
   - **Get Active Connections**: Lijst alle actieve netwerkverbindingen.
   - **Get System Info**: Verzamelt details over het besturingssysteem en hardware.
   - **List Running Processes**: Geeft een overzicht van actieve processen.
   - **Get Network Config**: Haalt netwerkinstellingen op, zoals IP, subnet, en gateway.
   - **Get WiFi Networks**: Lijst beschikbare wifi-netwerken.
   - **Get MAC Address**: Geeft het MAC-adres van het systeem weer.
   - **Get Disk Usage**: Toont schijfgebruik per partitie.
   - **List Files**: Lijst bestanden in een opgegeven directory.
   - **Get Current User**: Geeft de naam van de ingelogde gebruiker.
   - **List Users**: Lijst alle gebruikers op het systeem.
   - **Get OS Version**: Toont de versie van het besturingssysteem.
   - **Get Public IP**: Haalt het publieke IP-adres van het systeem op.
   - **Get Hostname**: Geeft de hostnaam van het systeem weer.
   - **Functie**: Zorgt voor uitgebreide systeeminformatie en netwerkanalyse.

### Testen
De modules zijn getest in een virtuele omgeving. Resultaten:
- **Backdoor**: Verbindingsopbouw en commandoverwerking functioneren naar behoren.
- **Portscanner**: Snelheid en accuraatheid van poortscans zijn goed.
- **System Enumeration**: Systeeminformatie en netwerkgegevens worden correct weergegeven.

---

## Reflectie

### **Wat werkt goed?**
- **Modulaire aanpak**: De structuur met dynamisch geladen modules bleek zeer effectief. Hierdoor konden functies eenvoudig worden toegevoegd of aangepast zonder wijzigingen aan de kerncode.
- **Threading in de Portscanner**: Het gebruik van threading zorgde voor aanzienlijk snellere poortscans. Dit bleek vooral nuttig bij grotere netwerken met veel poorten.
- **Integratie met GitHub**: Het automatisch ophalen van modules en uploaden van resultaten werkte vlekkeloos en vereenvoudigde het beheer.

### **Uitdagingen tijdens de ontwikkeling**
- **Synchronisatieproblemen**: Het gebruik van threading bracht aanvankelijk enkele racecondities en synchronisatieproblemen met zich mee. Door een globale lock en een betere thread-afhandeling toe te voegen, werden deze opgelost.
- **Testomgeving opzetten**: Het testen in een gecontroleerde en veilige omgeving was tijdrovend, maar essentieel om risico's te minimaliseren.

### **Wat ik heb geleerd**
- **Modulestructuur**: Het ontwerpen van een flexibele en uitbreidbare modulearchitectuur was een waardevolle oefening. Dit soort structuren is toepasbaar op veel andere projecten.
- **Threading en efficiëntie**: Het optimaliseren van prestaties via multithreading gaf inzicht in hoe concurrerende processen efficiënt kunnen worden afgehandeld.
- **GitHub-integratie**: Het dynamisch ophalen van modules en uploaden van resultaten gaf me inzicht in hoe versiebeheer en automatisering hand in hand kunnen gaan.

---

## Eindproducten

### **Code**
- Een volledig werkende Trojan met:
  - Configuratiebestand (`config.json`) dat modules en instellingen dynamisch beheert.
  - Drie aangepaste modules:
    1. **Backdoor**: Reverse shell-functionaliteit.
    2. **Portscanner**: Analyseert netwerken en scant poorten.
    3. **System Enumeration**: Verzamelt uitgebreide systeeminformatie.

### **GitHub-repository**
- **Structuur**:
  - **Modules**: Dynamisch geladen functies.
  - **Data**: Resultaten worden automatisch opgeslagen en geüpload naar de repository.
  - **Configuratie**: Configuratiebestand om instellingen en modules aan te passen.
- **Beveiliging**: De repository is privé gehouden om ongeautoriseerde toegang te voorkomen.

### **Demo**
Een korte video toont de werking van de Trojan.  
URL: [https://youtu.be/RH3AChMOpz4](https://youtu.be/RH3AChMOpz4)

