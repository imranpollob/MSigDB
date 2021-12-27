import pandas as pd
import sqlite3
from os.path import exists

db_file_name = 'msigdb.sqlite'
file_exists = exists(db_file_name)

parsed_file = pd.read_csv('parsed.csv')

con = sqlite3.connect(db_file_name)
cur = con.cursor()

if not file_exists:
    cur.execute('''CREATE TABLE gene_info
                (entrez_id, gene_name)''')

    cur.execute('''CREATE TABLE geneset_info
                (name, collection_name, orgnism)''')

    cur.execute('''CREATE TABLE associations
                (gene_id, geneset_id)''')

for index in range(len(parsed_file)):
    query = 'INSERT INTO gene_info (entrez_id, gene_name) VALUES ("' + str(parsed_file['Entrez ID'][index]) + '", "'+ parsed_file['Gene Name'][index] + '");'
    cur.execute(query)

    query = 'INSERT INTO geneset_info (name, collection_name, orgnism) VALUES ("' + str(parsed_file['Geneset Name'][index]) + '", "", "");'
    cur.execute(query)
    
    query = 'INSERT INTO associations (gene_id, geneset_id) VALUES ("' + str(parsed_file['Entrez ID'][index]) + '", "'+ parsed_file['Geneset Name'][index] + '");'
    cur.execute(query)

con.commit()
con.close()