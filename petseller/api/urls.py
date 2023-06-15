from django.urls import path,include
from home.views import *
urlpatterns = [
    path('animals/',AnimalView.as_view()),
    path('animal/<pk>/',AnimalDetailsView.as_view()),
    path('register/',RegisterApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('createAnimal/',AnimalCreateApi.as_view()),
    path('sell-animal/<slug:animal_slug>/', SellAnimalAPI.as_view()),
    path('purchase-animal/<str:animal_uuid>/', PurchaseAnimalAPI.as_view(), name='purchase_animal'),
    path('purchase/', PurchaseAPI.as_view(), name='purchase'),
]
