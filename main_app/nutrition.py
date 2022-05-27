import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


apiKey = 'pbtYsqSI82E2sTITqV3NBEeBUwsun0ifPoP5cs5a'
response = requests.get('https://api.nal.usda.gov/fdc/v1/food/746773?api_key=' + apiKey)
result = json.loads(response.text)
nutrients = {
    'name': '',
    'serving_size': '',
    'fat': 0,
    'calories': 0,
    'carbs': 0,
    'protein': 0,
    'fiber': 0,
    'sodium': 0,
    'cholesterol': 0,
    'sugar': 0,
}
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
        if i['nutrient']['name'] == 'Fiber, total dietary':
            nutrients['fiber'] = i['amount']
        if i['nutrient']['name'] == 'Sodium, Na':
            nutrients['sodium'] = i['amount']
        if i['nutrient']['name'] == 'Cholesterol':
            nutrients['cholesterol'] = i['amount']
        if i['nutrient']['name'] == 'Sugars, Total NLEA':
            nutrients['sugar'] = i['amount']
print(nutrients)