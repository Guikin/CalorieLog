from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('tracker/',views.tracker, name='tracker'),
    path('account/', include('django.contrib.auth.urls')),
    path('add/', views.add, name='add'),
    path('search/', views.search, name='search'),
    path('view/<int:id>/', views.display, name='view'),
    path('append/', views.append, name='append'),
    #path('tracker/<int:food_id>/delete',views.delete, name='delete_food'),

    # Auth
    path('accounts/signup/', views.signup, name='signup'),
    
    path('goals/<int:pk>/update/', views.GoalsUpdate.as_view(), name='goals_update')
]