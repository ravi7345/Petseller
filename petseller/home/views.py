from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import AnimalSerializer, PurchaseSerializer,RegisterApiSerializer,LoginApiSerializer,SellAnimalSerializer,PurchaseAnimalSerializer
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permission import IsPetOwnerPermission
from rest_framework import status
from django.db import transaction

class AnimalDetailsView(APIView):
    permission_classes = [IsAuthenticated,IsPetOwnerPermission]
    authentication_classes=[TokenAuthentication]

    def get(self,request,pk):
        try:
            queryset=Animal.objects.get(pk=pk)
            queryset.incrementViews()
            serializer=AnimalSerializer(queryset)
            return Response({
            'status':True,
            'massage':'data fetched with GET',
            'data':serializer.data
            })
        except Exception as e:
            print(e)
            return Response({
            'status':False,
            'massage':'Something went Wrong',
            'data':{}
        })
            

class AnimalView(APIView):
    permission_classes = [IsAuthenticated,IsPetOwnerPermission]
    authentication_classes=[TokenAuthentication]
    def get(self ,request):
        queryset=Animal.objects.all()

        if request.GET.get('search'):
            search=request.GET.get('search')
            queryset=queryset.filter(
                Q(animal_name__icontains=search) |
                Q(animal_description__icontains=search) |
                Q(animal_gender__iexact=search) |    
                Q(animal_breed__animal_Breed__icontains=search) |
                Q(animal_color__animal_color__icontains=search) 

            )
        serializer=AnimalSerializer(queryset,many=True)
        return Response({
            'status':True,
            'massage':'data fetched with GET',
            'data':serializer.data
        })
    def post(self ,request):
        return Response({
            'status':True,
            'massage':'data fetched with post'
        })
    def put(self ,request):
        return Response({
            'status':True,
            'massage':'data fetched with put'
        })
    def patch(self ,request):
        return Response({
            'status':True,
            'massage':'data fetched with patch'
        })

class RegisterApi(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterApiSerializer(data=data)

            if serializer.is_valid():
                user=User.objects.create(
                    username=serializer.data['username'],
                    email=serializer.data['email']
                )
                
                user.set_password(serializer.data['password'])
                user.save()
                return Response({
                    'massage': 'account crated',
                    'status':True,
                    'data':{}
                })  
            return Response({
                    'massage': 'key eror',
                    'status':False,
                    'data':serializer.errors
            })
        except Exception as e:
            print(e)


class LoginApi(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginApiSerializer(data=data)

            if serializer.is_valid():
                user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
                if user:
                    token,_=Token.objects.get_or_create(user=user)
                    
                    return Response({
                        "massage":"Login Successfullly",
                        "status":True,
                        "data":{
                            "token":str(token) 
                        }
                    })
                
                return Response({
                    'massage': 'Inavalid Password',
                    'status':False,
                    'data':{}
                })  
            return Response({
                    'massage': 'key eror',
                    'status':False,
                    'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                    'massage': 'Something went wrong',
                    'status':False,
                    'data':{} 
            })

class AnimalCreateApi(APIView):
    permission_classes = [IsAuthenticated,IsPetOwnerPermission]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        queryset=Animal.objects.filter(animal_owner=request.user)

        if request.GET.get('search'):
            search=request.GET.get('search')
            queryset=queryset.filter(
                Q(animal_name__icontains=search) |
                Q(animal_description__icontains=search) |
                Q(animal_gender__iexact=search) |    
                Q(animal_breed__animal_Breed__icontains=search) |
                Q(animal_color__animal_color__icontains=search) 

            )
        serializer=AnimalSerializer(queryset,many=True)
        return Response({
            'status':True,
            'massage':'data fetched with GET',
            'data':serializer.data
        })

    def post(self,request):       

        try:
            data=request.data
            serializer=AnimalSerializer(data=data)
            data['animal_owner']=request.user.id
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'Massage':"Animal Created Successfully",
                    'data':serializer.data

                })
            return Response({   
                'status':False,
                'Massages':'Invalid Data',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                    'massage': 'Something went wrong',
                    'status':False,
                    'data':{} 
            })
    def patch(self,request):
        try:
            data=request.data
            if data.get('id') is None:
                return Response({
                    'status':False,
                    'Massage':"Animal Id is required",
                    'data':{}

                })
            animal_obj=Animal.objects.filter(uuid=data.get('id'))
            if not animal_obj.exists(): 

                return Response({
                    'status':False,
                    'Massage':"Ivalid Animal id",
                    'data':{}

                })
            animal_obj=animal_obj[0]
            self.check_object_permissions(request,animal_obj)
            serializer=AnimalSerializer(data=data)
           
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'Massage':"Animal Updated",
                    'data':serializer.data

                })
            return Response({   
                'status':False,
                'Massages':'Invalid Data',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                    'massage': 'Something went wrong or you dont have permission to perform thi operation',
                    'status':False,
                    'data':{} 
            })

class SellAnimalAPI(APIView):
    permission_classes = [IsAuthenticated,IsPetOwnerPermission]
    authentication_classes=[TokenAuthentication]

    def post(self, request, animal_slug):
        try:
            animal = Animal.objects.get(animal_slug=animal_slug, animal_owner=request.user)
            serializer = SellAnimalSerializer(data=request.data)

            if serializer.is_valid():
                sell_obj, created = SellAnimal.objects.update_or_create(
                    animal=animal,
                    defaults={
                        'price': serializer.validated_data['price']
                    }
                )
                animal.is_for_sale = True
                animal.price = serializer.validated_data['price']
                animal.save()
                return Response({
                    'status':True,
                    'massage':'Thank you for selling your pet at our store',
                    'uuid': animal.uuid,
                    'data':serializer.data}, 
                    status=status.HTTP_201_CREATED)
            return Response({
                    "status":False,
                    "massage":"Your entered data is wrong Please Correct it!",
                    "data":serializer.errors
                },
                 status=status.HTTP_400_BAD_REQUEST)
        except Animal.DoesNotExist as e:
            print(e)
            return Response({
                "status":False,
                "massage":"Your entered data is wrong Please Correct it!",
                "data":'Animal not found or is not for sale',
                },
                  status=status.HTTP_404_NOT_FOUND)


class PurchaseAnimalAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def post(self, request, animal_uuid):
        try:
            animal = get_object_or_404(Animal, uuid=animal_uuid, is_for_sale=True)
            serializer = PurchaseAnimalSerializer(kdata=request.data)

            if serializer.is_valid():
                purchase_animal = PurchaseAnimal.objects.create(
                    animal=animal,
                    price=serializer.validated_data['price'],
                    buyer=request.user
                )
                animal.is_for_sale = False
                animal.is_sold=True
                animal.save()

                # Create a new Purchase instance
                purchase = Purchase.objects.create(
                    animal=animal,
                    buyer=request.user,
                    seller=animal.animal_owner,
                    price=serializer.validated_data['price']
                )

                return Response({
                    "status":True,
                    "massage":"Thank you purchasing",
                    "data":serializer.data
                },
                 status=status.HTTP_201_CREATED)
            return Response({
                    "status":False,
                    "massage":"Your entered data is wrong Please Correct it!",
                    "data":serializer.errors
                },
                 status=status.HTTP_400_BAD_REQUEST)
        except Animal.DoesNotExist as e:
            print(e)
            return Response({
                "status":False,
                "massage":"Your entered data is wrong Please Correct it!",
                "data":'Animal not found or is not for sale',
                },
                  status=status.HTTP_404_NOT_FOUND)


class PurchaseAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        purchases = Purchase.objects.filter(buyer=request.user).order_by('-created_at')
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)

        if serializer.is_valid():
            purchase = Purchase.objects.create(
                animal=serializer.validated_data['animal'],
                buyer=request.user,
                seller=serializer.validated_data['animal'].animal_owner,
                price=serializer.validated_data['price']
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
