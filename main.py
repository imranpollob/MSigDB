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

params = (
    ('filePath', '/msigdb/release/7.4/h.all.v7.4.symbols.gmt'),
)

requests.get('http://www.gsea-msigdb.org/gsea/msigdb/download_file.jsp', headers=headers, cookies=cookies, verify=False)
response = requests.get('https://data.broadinstitute.org/gsea-msigdb/msigdb/release/7.4/msigdb.v7.4.symbols.gmt', headers=headers)

with open('output.gmt', 'wb') as file:
    file.write(response.content)
