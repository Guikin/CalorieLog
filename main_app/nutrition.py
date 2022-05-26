import requests
import json

""" apiKey = 'pbtYsqSI82E2sTITqV3NBEeBUwsun0ifPoP5cs5a'
response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=' + apiKey + '&query=pear')
foods = []
result = json.loads(response.text)
for item in result['foods']:
    foods.append(item['description'])
    foods.append(item['fdcId'])
    if len(foods) > 50: break
it = iter(foods)
food_dict = dict(zip(it, it)) """


apiKey = 'pbtYsqSI82E2sTITqV3NBEeBUwsun0ifPoP5cs5a'
response = requests.get('https://api.nal.usda.gov/fdc/v1/food/167750?api_key=' + apiKey)
result = json.loads(response.text)
nutrients = {}
nutrients['name'] = result['description']
nutrients['serving_size'] = '100'
for i in result['foodNutrients']:
    if i['nutrient']['name'] == 'Total lipid (fat)':
        nutrients['fat'] = i['amount']
    if i['nutrient']['name'] == 'Energy' and i['nutrient']['unitName'] == 'kcal':
        nutrients['calories'] = i['amount']
    if i['nutrient']['name'] == 'Carbohydrate, by difference':
        nutrients['carbs'] = i['amount']
    if i['nutrient']['name'] == 'Protein':
        nutrients['protein'] = i['amount']

print(nutrients)
