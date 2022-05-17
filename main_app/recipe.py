import requests

api_url = 'https://api.calorieninjas.com/v1/recipe?query='
query = 'mushroom risotto'
response = requests.get(api_url + query, headers={'X-Api-Key': 'ORRHFQv5lyyiXX5IUN8dwg==jXOAvt1CW6wzwgfY'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)


