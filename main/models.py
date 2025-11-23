from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MainModel(models.Model):
    username=models.ForeignKey(User ,on_delete=models.CASCADE)
    #password=models.

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()

    def _str_(self):
        return f"{self.name} - {self.amount}"