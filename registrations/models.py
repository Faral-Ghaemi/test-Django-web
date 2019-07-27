from django.db import models
from django.utils import timezone
import datetime
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    def __str__(self):
        return self.name

class Membertype(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.name

class Chair(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=200)
    email= models.EmailField()
    phone= models.IntegerField()

    def __str__(self):
        return self.fullname

class League(models.Model):
    name=models.CharField(max_length=150)
    chair= models.ForeignKey(Chair, on_delete=models.SET_NULL, null=True, blank=True)
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name= models.CharField(max_length=50)
    league=models.ForeignKey('League', on_delete=models.CASCADE)
    Affiliation= models.CharField(max_length=50)
    Website= models.CharField(max_length=50)
    City= models.CharField(max_length=50)
    country = CountryField()
    quali = (
    ('Qualified','Qualified'),
    ('DISQualified', 'DISQualified'),
    ('Pendinng','Pendinng'),
    ('Finish','Finish'),
    )
    Status=models.CharField(max_length=40, choices=quali, default='Pendinng')
    usern = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    pay = (
    ('Paid','Paid'),
    ('Unpaid','Unpaid'),
    ('Cash on desk','Cash on desk'),
    )
    Payment_status = models.CharField(max_length=200,choices=pay,default="Unpaid")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('team_detail', args=[str(self.id)])

class Member(models.Model):
    team= models.ForeignKey(Team, on_delete=models.CASCADE,)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gander = (
    ('Male','Male'),
    ('Female', 'Female'),
    )
    types = (
    ('Student','Student'),
    ('Parent', 'Parent'),
    ('Supervisor', 'Supervisor'),
    )
    type=models.CharField(max_length=40, choices=types, default='Student')
    Gander=models.CharField(max_length=40, choices=gander, default='Male')
    email= models.EmailField(max_length=200)
    phone_number= models.CharField(max_length=30)
    date_of_birth=models.DateField()

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('team_detail', args=[str(self.id)])


class TC(models.Model):
    league= models.ForeignKey(League, on_delete=models.CASCADE,)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField()
    phone_number =models.IntegerField()

    def __str__(self):
        return self.first_name+" "+self.last_name

class Organiser(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField()
    phone_number=models.IntegerField()

    def __str__(self):
        return self.first_name+" "+self.last_name

class Champions(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Certificate(models.Model):
    championsTitle=models.ForeignKey(Champions, on_delete=models.CASCADE,)
    league=models.ForeignKey(League, on_delete=models.CASCADE,)
    team=models.ForeignKey(Team, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.championsTitle) +" "+str(self.league)
