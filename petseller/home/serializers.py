from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['uuid','category_name']
        read_only_fields = ['uuid']
class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalBreed
        fields=['uuid','animal_Breed']
        read_only_fields = ['uuid']
class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalColor
        fields=['uuid','animal_color']
        read_only_fields = ['uuid']
class AnimalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalImages
        fields=['uuid','animal_Images']
        read_only_fields = ['uuid']
class AnimalSerializer(serializers.ModelSerializer):
    animal_category= serializers.SerializerMethodField()       # CategorySerializer()
    animal_color=AnimalColorSerializer(many=True)
    animal_breed=AnimalBreedSerializer(many=True)
    seller = serializers.ReadOnlyField(source='seller.username')
    # animal_images=AnimalImagesSerializer(many=True)
    def get_animal_category(self,obj):
        return obj.animal_category.category_name
    
    def create(self, data):
        animal_breed=data.pop('animal_breed')
        animal_color=data.pop('animal_color')
        print(animal_breed)
        animal=Animal.objects.create(**data,animal_category=Category.objects.get(category_name='Dog'))

        for ab in animal_breed:
            animal_breed_obj=AnimalBreed.objects.get(animal_Breed=ab['animal_Breed'])
            animal.animal_breed.add(animal_breed_obj)
            
        for ac in animal_color:
            animal_color_obj=AnimalColor.objects.get(animal_color=ac['animal_color'])
            animal.animal_color.add(animal_color_obj)

        return animal
    
    def update(self,instance,data):
        if 'animal_breed' in data:
            animal_breed=data.pop('animal_breed')
            instance.animal_breed.clear()
            for ab in animal_breed:
                animal_breed_obj=AnimalBreed.objects.get(animal_Breed=ab['animal_Breed'])
                instance.animal_breed.add(animal_breed_obj)
            
        if 'animal_color' in data:
            animal_color =data.pop('animal_color')
            instance.animal_color.clear()
            for ac in animal_color:
                animal_color_obj=AnimalColor.objects.get(animal_color=ac['animal_color'])
                instance.animal_color.add(animal_color_obj)
            


        instance.animal_name=data.get('animal_name',instance.animal_name)
        instance.animal_description=data.get('animal_description',instance.animal_description)
        instance.animal_gender=data.get('animal_gender',instance.animal_gender)
        instance.save()
        return instance
    


    
    # def to_representation(self, instance):
    #     payload={
    #         "animal_category":instance.animal_category.category_name , 
    #         "animal_views":instance.animal_views,
    #         "animal_likes":instance.animal_likes,
    #         "animal_name":instance.animal_name,
    #         "animal_description":instance.animal_description,
    #     }
    #     return super().to_representation(instance)
    class Meta:
        model=Animal
        exclude=[
            'updated_at'
        ]
class AnimalLocarionSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalLocarion
        fields='__all__'

class RegisterApiSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if user.exists():
                raise serializers.ValidationError('Username is already taken ')
        if 'email' in data:
            user=User.objects.filter(email=data['email'])
            if user.exists():
                raise serializers.ValidationError('Email is already taken ')
        return data
    
class LoginApiSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if not user.exists():
                raise serializers.ValidationError('Username does not exists ')
        return data
    
class SellAnimalSerializer(serializers.ModelSerializer):
    # animal_name = serializers.CharField(source='animal.animal_name')
    # animal_description = serializers.CharField(source='animal.animal_description')
    # animal_gender = serializers.CharField(source='animal.animal_gender')
    # animal_breed = serializers.StringRelatedField(many=True, source='animal.animal_breed')
    # animal_color = serializers.StringRelatedField(many=True, source='animal.animal_color')
    # animal_category = serializers.StringRelatedField(source='animal.animal_category')
    # animal_owner = serializers.StringRelatedField(source='animal.animal_owner')
    
    class Meta:
        model = SellAnimal
        fields = ['uuid', 'animal',  'price', 'date_added']
        read_only_fields = ['uuid', 'animal', 'animal_name', 'animal_description', 'animal_gender', 'animal_breed', 'animal_color', 'animal_category', 'animal_owner', 'date_added']


class PurchaseAnimalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseAnimal
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('price', 'buyer', 'seller', 'animal')
