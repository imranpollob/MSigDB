import pandas as pd

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

    parsed_df = pd.DataFrame({
        'ID': [*range(counter, counter+id_len)], 
        'Entrez ID': geneset_entrez_ids, 
        'Gene Name': gene_names_per_set,
        'Geneset Name': geneset_name,
        'Geneset Link': geneset_link
    })

    main_parsed_df = main_parsed_df.append(parsed_df)

    counter += id_len

main_parsed_df.to_csv('parsed.csv')