from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food,Meal,Goals

import requests
import json
from django.views.generic.edit import UpdateView

# Create your views here.
def home(request):
    return render(request,'home.html')

def delete(request,food_id):
    delete_food = Food.objects.get(id=food_id).delete()
    
    return redirect('/tracker/')


#filtered all foods by meals for easier layout rendering
def tracker(request):
    all_food = Food.objects.filter(user = request.user)
    goals = Goals.objects.filter(user= request.user)
    if len(goals) == 0:
        init_goal = Goals.objects.create(user=request.user)
        init_goal.save()
    goals = Goals.objects.filter(user= request.user)    
    totalcal = 0
    totalcarbs = 0
    totalfat = 0
    totalprotein = 0
    totalsodium = 0
    totalsugar = 0

    
    # calculates total of nutrients for total table
    for food in all_food:
        totalcal = round((totalcal + food.calories),1)
        totalcarbs =round((totalcarbs+ food.carbohydrates),1)
        totalfat = round((totalfat + food.fat),1)
        totalprotein =round((totalprotein + food.protein),1)
        totalsodium = round((totalsodium + food.sodium),1)
        totalsugar = round((totalsugar + food.sugar),1)

    def fat_to_cal(amount):
        return amount * 9    
        
    def carb_prote_to_cal(amount):
        return amount * 4    

    #converts nutrients to cal for piechart 
    carbs_cal=carb_prote_to_cal(totalcarbs)
    protein_cal=carb_prote_to_cal(totalprotein)
    fat_cal=fat_to_cal(totalfat)   
    
    # calculates remaining difference for total table
    remaining_cal=0
    remaining_carbs=0
    remaining_protein=0
    remaining_fat=0

    percent_protein = 0
    percent_carbs = 0
    percent_fat = 0


    # calculates perentage for progress bar
    if len(goals)!=0 and len(all_food)!=0:
        for goal in goals:
            remaining_cal = round((goal.calories - totalcal),1)
            remaining_carbs = round((goal.carbs - totalcarbs),1) 
            remaining_protein = round((goal.protein - totalprotein),1)
            remaining_fat = round((goal.fat - totalfat),1)
            if(goal.protein != 0):
             percent_protein = round((totalprotein/goal.protein *100),1)
            if(goal.carbs !=0):
             percent_carbs = round((totalcarbs/goal.carbs *100),1)
            if(goal.fat): 
             percent_fat = round((totalfat/goal.fat *100),1)
        

    no_breakfast = None        
    no_lunch = None        
    no_dinner = None        
    no_snack = None

   
            
    # filter by meals for better layout rendering
    breakfast = Meal.objects.get(name='B').food_set.filter(user=request.user)
    if len(breakfast)==0:
        no_breakfast =True
    else:
        no_breakfast=False
    lunch = Meal.objects.get(name='L').food_set.filter(user=request.user)
    if len(lunch)==0:
        no_lunch =True
    else:
        no_lunch=False
    dinner = Meal.objects.get(name='D').food_set.filter(user=request.user)
    if len(dinner)==0:
        no_dinner =True
    else:
        no_dinner=False
    snack = Meal.objects.get(name='S').food_set.filter(user=request.user)
    if len(snack)==0:
        no_snack =True
    else:
        no_snack=False

       
    return render(request,'tracker.html',{
        'breakfast':breakfast,
        'lunch':lunch, 
        'dinner':dinner,
        'snack':snack,
        'all_food':all_food,
        'totalcal':totalcal, 
        'totalcarbs':totalcarbs,
        'totalfat':totalfat,
        'totalprotein':totalprotein,
        'totalsodium':totalsodium,
        'totalsugar':totalsugar,
        'goals':goals, 
        'remaining_cal':remaining_cal,
        'remaining_carbs':remaining_carbs,
        'remaining_protein':remaining_protein,
        'remaining_fat':remaining_fat, 
        'percent_protein':percent_protein,
        'percent_carbs':percent_carbs,
        'percent_fat':percent_fat,
        'carbs_cal':carbs_cal,
        'protein_cal':protein_cal,
        'fat_cal':fat_cal,

        'no_breakfast':no_breakfast,
        'no_lunch':no_lunch,
        'no_dinner':no_dinner,
        'no_snack':no_snack
        },)



def add(request,meal_id):
    return render(request, 'add.html', {'meal_id':meal_id})

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
    return render(request, 'add.html', {'food_dict':foods,})

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
        if i['nutrient']['name'] == 'Fiber, total dietary':
            nutrients['fiber'] = i['amount']
        if i['nutrient']['name'] == 'Sodium, Na':
            nutrients['sodium'] = i['amount']
        if i['nutrient']['name'] == 'Cholesterol':
            nutrients['cholesterol'] = i['amount']
        if i['nutrient']['name'] == 'Sugars, Total NLEA':
            nutrients['sugar'] = i['amount']
    return render(request, 'add.html', nutrients)

def append(request):
    if request.POST:
        data = request.POST.dict()
        if data['meals'] == 'breakfast':
            data['meals'] = 'B'
        elif data['meals'] == 'lunch':
            data['meals'] = 'L'
        elif data['meals'] == 'dinner':
            data['meals'] = 'D'
        else:
            data['meals'] = 'S'
        meal=Meal.objects.get(name=data['meals']).food_set.create(
            name=data['food_name'],
            sugar=data['sugar'],
            sodium=data['sodium'],
            fiber=data['fiber'],
            quantity= str(int(data['quantity'])*int(data['serving'])),
            fat=data['fats'],
            cholesterol=data['cholesterol'],
            protein=data['protein'],
            carbohydrates=data['carbs'],
            calories=data['calories'],
            user=request.user)

        # food = Food.objects.create(
        #     name=data['food_name'],
        #     sugar=data['sugar'],
        #     sodium=data['sodium'],
        #     fiber=data['fiber'],
        #     quantity= str(int(data['quantity'])*int(data['serving'])),
        #     fat=data['fats'],
        #     cholesterol=data['cholesterol'],
        #     protein=data['protein'],
        #     carbohydrates=data['carbs'],
        #     calories=data['calories'],
        #     user=request.user,
        # )
        print(meal)
        
    return redirect('/tracker/')
    
    
    
def explore(request):
    return render (request,'explore.html')    

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') # insert where to redirect
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class GoalsUpdate(UpdateView):
    model = Goals
    fields = ['calories', 'carbs', 'fat', 'protein']
    success_url = '/tracker/'