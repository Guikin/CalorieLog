from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food,Meal,Goals

# Create your views here.

def home(request):
    print('test')
    return render(request,'home.html')

#filtered all foods by meals for easier layout rendering
def tracker(request):
    all_food = Food.objects.all()
    goals = Goals.objects.all()
    totalcal = 0
    totalcarbs = 0
    totalfat = 0
    totalprotein = 0
    totalsodium = 0
    totalsugar = 0

    # calculates total of nutrients for total table
    for food in all_food:
        totalcal+= food.calories
        totalcarbs += food.carbohydrates
        totalfat += food.fat
        totalprotein += food.protein
        totalsodium += food.sodium
        totalsugar += food.sugar

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
    for goal in goals:
        remaining_cal = goal.calories - totalcal 
        remaining_carbs = goal.carbs - totalcarbs 
        remaining_protein = goal.protein - totalprotein
        remaining_fat = goal.fat - totalfat
        percent_protein = round(totalprotein/goal.protein *100)
        percent_carbs = round(totalcarbs/goal.carbs *100)
        percent_fat = round(totalfat/goal.fat *100)
        

    # filter by meals for better layout rendering
    breakfast = Meal.objects.get(name='B').food_set.all()
    lunch = Meal.objects.get(name='L').food_set.all()
    dinner = Meal.objects.get(name='D').food_set.all()
    snack = Meal.objects.get(name='S').food_set.all()


    return render(request,'tracker.html',{
        'breakfast':breakfast,
        'lunch':lunch, 
        'dinner':dinner,
        'snack':snack,
        'all_food':all_food ,
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
        'fat_cal':fat_cal
        },)

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
