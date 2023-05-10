Skript funguje jako scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu.
Po zadání odkazu, jako prvního argumentu, na libovolný územní celek z tohoto odkazu: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ 
vyscrapuje výsledky hlasování pro všechny obce tohoto územního celku.
Druhým argumentem je pak jméno výstupního souboru (př. vysledky_prostejov.csv).
Skript se spouští ve tvaru: 
projekt_3.py [url územního celku] [název výstupního csv souboru]

Potřebné knihovny si nainstalujete ze souboru requirements.txt pomocí příkazu: `pip install -r requirements.txt`
