# Box 2 versus Box 3

Wat is het?

Beleggen in de BV (Box 2) of in prive (Box 3) -- het is anno 2024 een lastige discussie. De Python-app in deze repo rekent de uitkomsten tussen de twee modellen door op basis van een aantal assumpties en 'input'. De input bestaat uit:
- waarde aandelen & rendement;
- waarde obligaties & rendement;
- waarde vastgoed & rendement.

Het rekenwerk is gebaseerd op de Box2 en Vpb tarieven en schijven anno 2024 en de uitgangspunten van de Wet werkelijk rendement Box 3 (alle vermogenswinst jaarlijks belast ongeacht gerealiseerd m.u.v. onroerend goed). Onroerend goed stijgt in het model jaarlijks in waarde met de inflatie. 

In deze repo de volgende files:
- boxer.py
- app.py
- .xlsx file

Boxer.py is het rekenmodel. App.py is de streamlit app. De *.xslx file is de blauwdruk op basis waarvan het python model is gebouwd. Het *.xlsx model bevat ook de beschrijving van de formules; de resultaten van het python model komen grotendeels overeen met het *.xlsx model.

De python files hebben louter de streamlit package nodig:
pip install streamlit

De app kan vervolgens gestart worden met 'streamlit run app.py'. 

De app is ook online beschikbaar via Streamlit Community:

https://box2vs3-yeogyf5ym9rtdr5egu8wib.streamlit.app
