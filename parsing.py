import pandas as pd
from bs4 import BeautifulSoup
import requests

cookies = {
    'JSESSIONID': 'B6BE93A3B62F8F9CB8866C24DED59DF1',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.gsea-msigdb.org/gsea/downloads.jsp',
    'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8,ar;q=0.7',
}

file_name = 'h.all.v7.4'

requests.get('http://www.gsea-msigdb.org/gsea/msigdb/download_file.jsp', headers=headers, cookies=cookies, verify=False)
symbol_res = requests.get(f'https://data.broadinstitute.org/gsea-msigdb/msigdb/release/7.4/{file_name}.symbols.gmt', headers=headers)
entrez_res = requests.get(f'https://data.broadinstitute.org/gsea-msigdb/msigdb/release/7.4/{file_name}.entrez.gmt', headers=headers)

with open(f'{file_name}.symbols.gmt', 'wb') as file:
    file.write(symbol_res.content)

with open(f'{file_name}.entrez.gmt', 'wb') as file:
    file.write(entrez_res.content)

lines_from_entrez = []
lines_from_symbol = []

with open(f'{file_name}.entrez.gmt') as f:
    lines_from_entrez = f.readlines()

with open(f'{file_name}.symbols.gmt') as f:
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