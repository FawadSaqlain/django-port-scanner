from django.urls import path
from . import views

app_name = 'portscanner'

urlpatterns = [
    path('showport/', views.showport, name='showport'),
    path('openport/', views.openport, name='openport'),
    path('closeport/', views.closeport, name='closeport'),
    path('manu/', views.manu, name='manu'),
]
