from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core import validators
# Create your models here.


category_choices= (
    ('MB', "Mobiles"),
    ('TY', "Toys"),
    ('LP', "Laptop"),
    ('EC', "Education"),
    ('HD', "Headphones"),
    ('WT', "Watch"),
    ('PC', "Personal Care"),
    ('SH', "Shoes"),
)
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

nations = (("China","China"),("India ","India"),("USA","USA"),("UAE","UAE"),("UK","UK"),("Srilanka","Srilanka"))



class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.TextField(choices=category_choices, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
def validate_mobile(value):
    num = value
    digits = [int(x) for x in str(num)]
    print(len(digits))
    if len(digits) != 10:
        raise ValidationError("Enter Mobile number properly.!")

def val_pin(value):  
    num = value
    num_str = str(num)
    print(len(num_str))
    if len(num_str) != 6:
        raise ValidationError("Enter valid Pin code.!")

    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    mobile = models.IntegerField(validators=[validate_mobile])
    pincode = models.IntegerField(validators=[val_pin])
    state = models.CharField(choices=state_choices, max_length=50, blank=True, null=True)
    country = models.CharField(choices=nations, max_length=25, default='India')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

