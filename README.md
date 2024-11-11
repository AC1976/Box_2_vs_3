# Box 2 versus Box 3

Nederlandse inkomstenbelastingplichtigen met vermogen in Box 3 wordt soms geadviseerd het vermogen middels een kapitaalstorting in te brengen in een 'Spaar BV' of 'Beleggings BV'. Het rendement op het vermogen groeit dan aan in de BV tegen het lagere vennootschapbelastingtarief. Ook de toepassing van goed koopmansgebruik bij de fiscale winstbepaling van de BV zou, aldus de proponenten, zorgen voor een liquiditeitsvoordeel ten opzichte van Box 3, wat zich weerspiegelen zou in een uiteindelijk hoger netto rendement na belasting. De keerzijde van deze redenering is de onvermijdelijke Box 2 heffing bij uitkering van de winstreserves uit de BV aan de aandeelhouder. Die claim is anno 2024 niet af te schudden door emigratie of zelfs overlijden (zelfs indien na emigratie). 

De vraag komt dus op wanneer zo'n BV op de Box 2 route fiscaal voordeliger is. Met bijgaande modellen kan dit eenvoudig worden uitgerekend aan de hand van een aantal veronderstellingen. 

## Toelichting modellen

De modellen maken onderscheid tussen beleggingen in aandelen, obligaties en/of onroerend goed. Voor aandelen geeft men zowel het verwachte dividendrendement op, alsmede de verwachte koerstijging per jaar. Voor obligaties de effectieve rente ('yield') en voor onroerend goed de netto huurinkomsten. De modellen rekenen met een waardestijging van het onroerend goed gelijk aan de jaarlijkse inflatie. 

In het Box 3 model, gebaseerd op de uitgangspunten van het wetsvoorstel Werkelijk rendement Box 3 dat naar verwachting per 2027 in werking treedt, worden alle dividend, rente, huurinkomsten en -- gerealiseerde en ongerealiseerde -- vermogenswinsten op de aandelen jaarlijks in de Box 3 heffing betrokken. De vermogenswinst op het onroerend goed wordt pas belast bij verkoop. 

In het Box 2 model, gebaseerd op goed koopmansgebruik, worden alle dividend, rente en huurinkomsten gerekend tot de jaarwinst. Vermogenswinsten op de aandelen worden alleen jaarlijks in de winst betrokken indien de parameter voor 'mark-to-market' (mtm) op 'True' wordt gezet. Wordt deze parameter op False gezet, dan wordt de vermogenswinst op de aandelen pas bij verkoop in de winst betrokken. Conform het Niederwertz-beginsel wordt het onroerend goed op kostprijs gewaardeerd.

De Box 2 en Vpb tarieven en schijven kunnen worden geconfigureerd naar wens, maar staan als default op de huidige stand. Het Box 3 tarief staat als default op 36% en kan ook worden gewijzigd. De parameter 'partners' kan op True of False worden gezet. Indien 'true' dan wordt de eerste schijf in de AB heffing verdubbeld, net zoals de belastingvrije inkomensgrens voor Box 3.

## Gebruik

De modellen zijn beschikbaar gemaakt als een streamlit app. Streamlit lanceert een server op de lokale computer, waarna men met een browser naar de streamlit app op deze server navigeert. In de browser vult men dan de benodigde gegevens in, waarna de app op basis van de hierboven beschreven modellen het rekenwerk uitvoert. De app presenteert de uitkomsten als een aantal spreadsheets die als *.csv bestand kunnen worden gedownload en daarna geopend in een spreadsheetprogramma zoals Excel. De app maakt ook een aantal grafieken op de uitkomsten direct op het scherm te vergelijken.

## Installeren

tbc
