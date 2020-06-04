import requests
from collections import OrderedDict
import pandas as pd
import psycopg2
import io
import numpy as np

url = 'https://query.wikidata.org/sparql'
query = """
SELECT DISTINCT ?stateLabel ?county ?countyLabel ?area ?unitLabel ?population WHERE {
  ?state wdt:P31 wd:Q35657 .
  ?state wdt:P150 ?county . 
  ?county p:P2046 ?stmnode .
  ?stmnode psv:P2046 ?valuenode .
  ?valuenode     wikibase:quantityAmount     ?area.
  ?valuenode     wikibase:quantityUnit       ?unit.
  ?county wdt:P1082 ?population 

 SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
 }"""
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()



counties = []
for item in data['results']['bindings']:
    if item['county']['value'] == 'http://www.wikidata.org/entity/Q107126' and item['unitLabel']['value'] == 'square mile'\
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q26907' and item['population']['value'] != '2311'\
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q39450' and item['area']['value'] != '4420' \
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q494624' and item['unitLabel']['value'] == 'square mile' \
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q26807' and item['unitLabel']['value'] == 'square mile' \
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q488659' and item['unitLabel']['value'] == 'square mile' \
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q421970' and item['unitLabel']['value'] == 'square mile' \
            or item['county']['value'] == 'http://www.wikidata.org/entity/Q505515' and item['unitLabel']['value'] == 'square mile' :
        continue

    if item['unitLabel']['value'] == 'square mile':
            item['area']['value'] = float(item['area']['value']) * 2.58998811
            item['unitLabel']['value'] = 'square kilometre'
    counties.append(OrderedDict({
        label : item[label]['value'] if label in item else None
        for label in ['county', 'stateLabel', 'countyLabel',
                      'area', 'population']}))

df = pd.DataFrame(counties)
df.set_index('county', inplace=True)
df = df.astype({'area': float, 'population': float})
df.head()

r.close()

query2 = """
SELECT ?c ?cLabel ?countyLabel ?area ?unitLabel ?population WHERE {
  ?c wdt:P31 wd:Q1352230 .
  ?c wdt:P31 wd:Q783733 .
  ?c p:P2046 ?stmnode .
  ?stmnode psv:P2046 ?valuenode .
  ?valuenode     wikibase:quantityAmount     ?area.
  ?valuenode     wikibase:quantityUnit       ?unit.
  ?c wdt:P1082 ?population .

 SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
 }"""
r = requests.get(url, params={'format': 'json', 'query': query2})
data2 = r.json()
counties=[]
for item in data2['results']['bindings']:
    if item['unitLabel']['value'] == 'square mile':
        item['area']['value'] = float(item['area']['value']) * 2.58998811
        item['unitLabel']['value'] = 'square kilometre'
    counties.append(OrderedDict({
        label : item[label]['value'] if label in item else 'Unknown'
        for label in ['c', 'cLabel', 'countyLabel',
                      'area', 'population']}))

counties.append(OrderedDict([('c', 'https://www.wikidata.org/wiki/Q11703'), ('cLabel', 'Virgin Islands'), ('countyLabel', 'Unknown'), ('area', '346.36'), ('population', '104901')]))
counties.append(OrderedDict([('c', 'https://www.wikidata.org/wiki/Q3551781'), ('cLabel', 'District of Columbia'), ('countyLabel', 'District of Columbia'), ('area', '177'), ('population', '672228')]))

df2 = pd.DataFrame(counties)
df2.set_index('c', inplace=True)
df2 = df2.astype({'area': float, 'population': float})
df2.head()
r.close()

conn = psycopg2.connect(host="localhost", port = 5432, database="covid", user="daniellechamberlain", password="postgres")
cur = conn.cursor()

cur.execute("""
            CREATE TABLE Counties_Area_Pop (
            state_Label VARCHAR(255) NOT Null,
            county_Label VARCHAR(255),
            area_km2 float4,
            population float4)"""
            )

output = io.StringIO()
df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'Counties_Area_Pop', null="") # null values become ''
conn.commit()

output = io.StringIO()
df2.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'Counties_Area_Pop', null="") # null values become ''
conn.commit()
cur.close()
conn.close()

