from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('tracker/',views.tracker, name='tracker'),
    path('account/', include('django.contrib.auth.urls')),
    path('add/', views.add, name='add'),
    path('search/', views.search, name='search'),

    # Auth
    path('accounts/signup/', views.signup, name='signup')
]