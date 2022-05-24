import requests
query = 'italian wedding soup'
api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'ORRHFQv5lyyiXX5IUN8dwg==QG7GGZedGnedFum3'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)


