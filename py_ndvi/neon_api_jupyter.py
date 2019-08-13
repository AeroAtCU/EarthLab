import requests
import json
from pprint import pprint

SITECODE = "ABBY" #the site code for Abby Road
PRODUCTCODE = "DP1.00098.001" #the product code for Relative Humidity
SERVER = "http://data.neonscience.org/api/v0/" #the current server address

site_response = requests.get(SERVER + 'sites/' + SITECODE)

site_response_json = site_response.json()
#print(json.dumps(site_response_json, indent=2)) #using json.dumps for formatting


data_products = site_response_json['data']['dataProducts']

#use a list comprehension here if you're feeling fancy
for data_product in data_products:
	if (data_product['dataProductCode'] == PRODUCTCODE):
		months = data_product['availableMonths']

#print(months)

data_response = requests.get(SERVER + 'data/' + PRODUCTCODE + '/' + SITECODE + '/' + '2016-04')
data_response_json = data_response.json()
# print(json.dumps(data_response_json, indent=2))

for line in data_response_json['data']['siteCode']:
    print(line)
    print()

for line in data_response_json['data']:
    print(line)
    print()

print(data_response_json['data']['files'][4]['url'])

#so it goes: data_response_json -> files -> index[x] -> url   
#files is a list inside the the dict data_response_json
#each element of files is a dict with 4 strings

#data_response_json: dict
#- files: list
#  - index 0: dict
#    - crc32: str
#    - name: str
#    - size: str
#    - url: str
#  - index ...: dict
#- month: str
#- productCode: str
#- siteCode: str

#_urls = data_response_json['data']['urls']
#print(json.dumps(data_urls, indent=2))
#csv_data_response = requests.get('https://neon-prod-pub-1.s3.data.neonscience.org/NEON.DOM.SITE.DP1.00098.001/PROV/ABBY/20160401T000000--20160501T000000/expanded/NEON.D16.ABBY.DP1.00098.001.000.040.030.RH_30min.2016-04.expanded.20171026T095524Z.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20190813T161754Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Credential=pub-internal-read%2F20190813%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=c93a9bdce0b601d210ab93a9e89e84b98c87e57e2664c5cd51e842d1e59f0461')
#print(csv_data_response.text)

# ---------- #

#pprint(dir(data_response_json))
#type(data_response_json)
#if (isinstance(data_response_json, pd.DataFrame)): # can be used to check type
#print(type(data_response_json)) # print variable type (int, long, dict etc)
#print(data_response_json.keys()) # print dict field names (aka keys)

# ---------- #
