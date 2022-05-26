from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('tracker/',views.tracker, name='tracker'),
    path('explore/',views.explore, name='explore'),
    path('account/', include('django.contrib.auth.urls')), 

    # Auth
    path('accounts/signup/', views.signup, name='signup'),
    
    path('goals/<int:pk>/update/', views.GoalsUpdate.as_view(), name='goals_update')
]