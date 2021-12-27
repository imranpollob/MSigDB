import pandas as pd
import sqlite3
import os
from os.path import exists

db_file_name = 'msigdb.sqlite'
file_exists = exists(db_file_name)

if file_exists:
    os.remove(db_file_name)

parsed_file = pd.read_csv('parsed.csv')

con = sqlite3.connect(db_file_name)
cur = con.cursor()
    
cur.execute('''CREATE TABLE gene_info
                (entrez_id, gene_name)''')

cur.execute('''CREATE TABLE geneset_info
            (name, collection_name, orgnism)''')

cur.execute('''CREATE TABLE associations
            (gene_id, geneset_id)''')
    

for index in range(len(parsed_file)):
    query = 'INSERT INTO gene_info (entrez_id, gene_name) VALUES ("' + str(parsed_file['Entrez ID'][index]) + '", "'+ parsed_file['Gene Name'][index] + '");'
    cur.execute(query)

    query = 'INSERT INTO associations (gene_id, geneset_id) VALUES ("' + str(parsed_file['Entrez ID'][index]) + '", "'+ parsed_file['Geneset Name'][index] + '");'
    cur.execute(query)

unique_genesets = parsed_file.drop_duplicates(subset=['Geneset Name'])

for i, unique_geneset in unique_genesets.iterrows():
    query = 'INSERT INTO geneset_info (name, collection_name, orgnism) VALUES ("' + str(unique_geneset['Geneset Name']) + '", "' + unique_geneset['Collection Name'] +'", "'+ unique_geneset['Organism'] +'");'
    cur.execute(query)

con.commit()
con.close()