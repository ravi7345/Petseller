from django.urls import path,include
from home.views import *
urlpatterns = [
    path('animals/',AnimalView.as_view()),
    path('animal/<pk>/',AnimalDetailsView.as_view()),
    path('register/',RegisterApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('createAnimal/',AnimalCreateApi.as_view()),
    
    path('purchase-animal/<str:animal_uuid>/', PurchaseAnimalAPI.as_view(), name='purchase_animal'),
    path('purchase/', PurchaseAPI.as_view(), name='purchase'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('animal-breeds/', AnimalBreedListView.as_view(), name='animal-breed-list'),
    path('animal-breeds/<int:pk>/', AnimalBreedDetailView.as_view(), name='animal-breed-detail'),
    path('animal-colors/', AnimalColorListView.as_view(), name='animal-color-list'),
    path('animal-colors/<int:pk>/', AnimalColorDetailView.as_view(), name='animal-color-detail'),

    path('animal-locations/', AnimalLocationListView.as_view(), name='animal-location-list'),
    path('animal-locations/<int:pk>/', AnimalLocationDetailView.as_view(), name='animal-location-detail'),
    path('animal-images/', AnimalImagesListView.as_view(), name='animal-images-list'),
    path('animal-images/<int:pk>/', AnimalImagesDetailView.as_view(), name='animal-images-detail'),



    path('sell-animals/', SellAnimalListView.as_view(), name='sell-animal-list'),
    path('sell-animals/<int:pk>/', SellAnimalDetailView.as_view(), name='sell-animal-detail'),
    


]
