from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food,Meal,Goals
import requests
import json

def home(request):
    return render(request,'home.html')


#filtered all foods by meals for easier layout rendering
def tracker(request):
    all_food=Food.objects.all()
    breakfast = Meal.objects.get(id=1).food_set.all()
    lunch = Meal.objects.get(id=2).food_set.all()
    dinner = Meal.objects.get(id=3).food_set.all()
    snack = Meal.objects.get(id=4).food_set.all()
    return render(request,'tracker.html',{'breakfast':breakfast,'lunch':lunch, 'dinner':dinner,'snack':snack,'all_food':all_food})

def add(request):
    return render(request, 'add.html')

""" def search(request):
    query = request.GET['query']
    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query":query}
    headers = {
        "X-RapidAPI-Host": "calorieninjas.p.rapidapi.com",
        "X-RapidAPI-Key": "b7cdab9648msh48c8c9f16a4b05dp1a5a8ajsn60e2f660bcac"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    dictionary = json.loads(response.text)
    items = dictionary['items'][0]
    if not items:
        items = {
                    'sugar_g': '', 
                    'fiber_g': '', 
                    'serving_size_g': '', 
                    'sodium_mg': '', 
                    'name': '---', 
                    'potassium_mg': '',
                    'fat_saturated_g': '',
                    'fat_total_g': '-g',
                    'calories': '--',
                    'cholesterol_mg': '',
                    'protein_g': '-g',
                    'carbohydrates_total_g': '-g'
        }
    print(items)
    return render(request, 'add.html', items) """

def search(request):
    query = request.GET['query']
    apiKey = 'pbtYsqSI82E2sTITqV3NBEeBUwsun0ifPoP5cs5a'
    response = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=' + apiKey + '&query=' + query)
    foods = []
    result = json.loads(response.text)
    for item in result['foods']:
        dictionary = {}
        dictionary['name'] = item['description']
        dictionary['id'] = item['fdcId']
        foods.append(dictionary)
        if len(foods) > 50: break
    return render(request, 'add.html', {'food_dict':foods})

def display(request, id):
    apiKey = 'pbtYsqSI82E2sTITqV3NBEeBUwsun0ifPoP5cs5a'
    response = requests.get('https://api.nal.usda.gov/fdc/v1/food/' + str(id) + '?api_key=' + apiKey)
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
    return render(request, 'add.html', nutrients)
    
    

# input this into the mainDataModel's(CreateView); below
    # def form_valid(self,form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

# input this into the mainDataModel's_index(request)
    # mainDataModels = MainDataModel.objects.filter(user=request.user)
    # return render(request, 'mainDataModels/INDEX.html', { 'mainDataModels': mainDataModels})

# remember to wrap variables in '@login_required' to protect the data
# wrap class based views (CreateView, UpdateView etc..) in 'LoginRequiredMixin'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('After Signup whereeee??') # insert where to redirect
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
