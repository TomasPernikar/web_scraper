"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Pernikář
email: tomworld@seznam.cz
discord: Tomáš P.#9699
"""

import requests
from bs4 import BeautifulSoup
import csv
import os

def get_region_links(url: str) -> list:
    """
    Získá odkazy na všechny obce v daném územním celku.
    Args:
        url: Odkaz na stránku s územními celky
    Returns: 
        Seznam odkazů na stránky s výsledky pro jednotlivé okresy v daném kraji
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for row in soup.find_all('td', {'class': 'cislo'}):
            links.append({
            'name': row.find_all('a')[0].text,
            'url': 'https://volby.cz/pls/ps2017nss/' + row.find_all('a')[0]['href']
            })
        return links
    else:
        quit()

def get_results_for_region(url: str, output_file: str) -> None:
    """
    Získá výsledky hlasování pro všechny obce ve vybraném regionu a uloží je do souboru CSV.
    Args:
        url (str): Adresa URL na územní celek, který má být zpracován.
        output_file (str): Cesta a název výstupního souboru typu CSV.
    Returns:
        None
    """
    # Získání odkazů na stránky s výsledky pro jednotlivé obce v daném regionu
    region_links = get_region_links(url)
    # Procházení jednotlivých odkazů na obecní stránky, získání jména obce a volebních výsledků
    data = []
    for link in region_links:
        response = requests.get(link['url'])
        soup = BeautifulSoup(response.text, 'html.parser')
        # Najde název obce
        names = soup.find('div', {'class': 'topline', 'id': 'publikace'})
        rows_names = names.find_all('h3')
        nazev_obce = rows_names[2].text.split(": ")[1]
        # Najde tabulku obsahující výsledky pro všechny obce v regionu
        table = soup.find('table', {'class': 'table', 'id': 'ps311_t1'})
        # Získá řádky tabulky (s výjimkou řádku s hlavičkou)
        rows = table.find_all('tr')[2:]

        # Projde řádky a získá údaje pro každou obec
        for row in rows:
            # Vezme sloupce řádku
            columns = row.find_all('td', {'class': 'cislo'})
            # Získá údaje ze sloupců a uloží je do proměnných
            kod_obce = link['name']
            volici_v_seznamu = columns[3].text
            vydane_obalky = columns[4].text
            platne_hlasy = columns[7].text

            # Získá jména stran s počty hlasů
            party_table = soup.find('div', {'id': 'outer'})
            party_rows = party_table.find_all('tr')[2:]
            hlasy = []
            parties = []
            for row in party_rows:
                parties_names = row.find_all('td', {'class': 'overflow_name', 'headers': 't1sa1 t1sb2' })
                for party in parties_names:
                    party_name = party.text
                    parties.append(party_name)
                parties_names2 = row.find_all('td', {'class': 'overflow_name', 'headers': 't2sa1 t2sb2' })
                for party in parties_names2:
                    party_name = party.text
                    parties.append(party_name)
                party_columns = row.find_all('td', {'class': 'cislo', 'headers': 't1sa2 t1sb3' })
                for strana in party_columns:
                    hlas = strana.text
                    hlasy.append(hlas)
                party_columns2 = row.find_all('td', {'class': 'cislo', 'headers': 't2sa2 t2sb3' })
                for strana in party_columns2:
                    hlas = strana.text
                    hlasy.append(hlas)
            # Uloží získané údaje do hlavního seznamu
            radek = [kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy] + hlasy
            data.append(radek)      
    # Zapíše získané údaje do csv souboru
    # Přidá cestu do aktuálního pracovního adresáře k názvu výstupního souboru
    output_file = os.path.join(os.getcwd(), output_file)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        headline = [
            'Kód obce', 
            'Obec', 
            'Počet registrovaných voličů', 
            'Vydané obálky',
            'Platné hlasy' 
        ] + parties
        writer.writerow(headline)
        writer.writerows(data)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Použití: projekt_3.py \"[url územního celku]\" \"[název výstupního csv souboru]\"")
    else:
        url = sys.argv[1]
        output_file = sys.argv[2]
        print(f"Výsledky naleznete v souboru {output_file} v aktuálním adresáři.")
        get_results_for_region(url, output_file)
