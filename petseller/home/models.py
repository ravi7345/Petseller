from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from .choices import GENDER_CHOICES
import uuid
from django.utils.text import slugify


class BaseModel(models.Model):
    uuid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    class Meta:
        abstract=True

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.category_name
class AnimalBreed(BaseModel):
    animal_Breed=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.animal_Breed
class AnimalColor(BaseModel):
    animal_color=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.animal_color



class Animal(BaseModel):
    animal_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animal")
    animal_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="animal_category")
    animal_views = models.IntegerField(default=0)
    animal_likes = models.IntegerField(default=1)
    animal_name = models.CharField(max_length=100)
    animal_description = models.TextField()
    animal_slug = models.SlugField(max_length=100, unique=True)
    animal_gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    animal_breed = models.ManyToManyField(AnimalBreed, null=True)
    animal_color = models.ManyToManyField(AnimalColor, null=True)
    is_sold = models.BooleanField(default=False)
    is_for_sale = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        uid = str(uuid.uuid4()).split('-')
        self.animal_slug = slugify(self.animal_name) + '-' + uid[0]
        super(Animal, self).save(*args, **kwargs)

    def incrementViews(self):
        self.animal_views += 1
        self.save()

    def incrementLikes(self):
        self.animal_likes += 1
        self.save()

    def __str__(self) -> str:
        return self.animal_name

    class Meta:
        ordering = ['animal_name']
class AnimalLocarion(BaseModel):
    animal=models.ForeignKey(Animal,on_delete=models.CASCADE,related_name="animal_location")
    location=models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.animal.animal_name} Location'
class AnimalImages(BaseModel):
    animal=models.ForeignKey(Animal,on_delete=models.CASCADE,related_name="animal_images")
    animal_Images=models.ImageField(upload_to="animal")
    def __str__(self) -> str:
        return f'{self.animal.animal_name} Images'




class SellAnimal(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="sell_animal")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # is_sold = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.animal.animal_name + ' for ' + str(self.price)

class PurchaseAnimal(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)

class Purchase(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='purchase_animal')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.buyer.username} purchased {self.animal.animal_name} from {self.seller.username}'
