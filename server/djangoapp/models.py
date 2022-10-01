from django.db import models
from django.utils.timezone import now


#  Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(max_length=500)
    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description

# Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    cardealer = models.IntegerField()
    name = models.CharField(null=False, max_length=50, default='')
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    OTHER = 'other'
    CAR_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (OTHER, 'Other')
        ]
    cartype = models.CharField(
        null=False,
        max_length=20,
        choices=CAR_CHOICES,
        default=SEDAN
    )
    caryear = models.DateField()
    def __str__(self):
        return "Name: " + self.name + "," + "Type: " + self.cartype
