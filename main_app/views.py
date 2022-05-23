from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return render(request,'home.html')

def tracker(request):
    return render(request,'tracker.html')


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
