from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('tracker/',views.tracker, name='tracker'),
    path('explore/',views.explore, name='explore'),
    path('account/', include('django.contrib.auth.urls')),

    # Auth
    path('accounts/signup/', views.signup, name='signup')
]