from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food,Meal,Goals

# Create your views here.

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

def explore(request):
    return render (request,'explore.html')    


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
