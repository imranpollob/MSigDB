import pandas as pd
from bs4 import BeautifulSoup
import requests

lines_from_entrez = []
lines_from_symbol = []

with open('h.all.v7.4.entrez.gmt') as f:
    lines_from_entrez = f.readlines()

with open('h.all.v7.4.symbols.gmt') as f:
    lines_from_symbol = f.readlines()

main_parsed_df = pd.DataFrame([], columns=['ID', 'Entrez ID', 'Gene Name', 'Geneset Name', 'Geneset Link'])
counter = 0

for line, symbol_line in zip(lines_from_entrez, lines_from_symbol):
    line = line.replace("\n", "")
    symbol_line = symbol_line.replace("\n", "")
    geneset_info = line.split("\t")
    gene_names = symbol_line.split("\t")

    geneset_name = geneset_info[0]
    geneset_link = geneset_info[1]
    geneset_entrez_ids = geneset_info[2:]
    gene_names_per_set = gene_names[2:]
    id_len = len(geneset_entrez_ids)
    geneset_collection_name = ""
    geneset_organism = ""


    res = requests.get(geneset_link)
    soup = BeautifulSoup(res.content, 'html.parser')
    table_data = soup.find_all("table", {"class": "lists4"})[0]
    
    for table_row in table_data.find_all("tr"):
        if table_row.find('th') and table_row.th.text == "Collection":
            geneset_collection_name = table_row.td.text
        if table_row.find('th') and table_row.th.text == "Organism":
            geneset_organism = table_row.td.text

    parsed_df = pd.DataFrame({
        'ID': [*range(counter, counter+id_len)], 
        'Entrez ID': geneset_entrez_ids, 
        'Gene Name': gene_names_per_set,
        'Geneset Name': geneset_name,
        'Geneset Link': geneset_link,
        'Collection Name': geneset_collection_name,
        'Organism': geneset_organism
    })

    main_parsed_df = main_parsed_df.append(parsed_df)

    counter += id_len

main_parsed_df.to_csv('parsed.csv')