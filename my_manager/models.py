from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class trade(models.Model):
        name = models.CharField(max_length=200,null=True)

        def __str__(self):
          return self.name

class role(models.Model):
        name = models.CharField(max_length=200,null=True)
        
        def __str__(self):
          return self.name

class Coordinator(models.Model):
    my_user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length = 200,null=True)
    phone = models.CharField(max_length=200,null=True,blank=True)
    

    def __str__(self):
        return self.name

class Manager(models.Model):
     my_user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
     name = models.CharField(max_length = 200,null=True) 
     phone = models.CharField(max_length=200,null=True,blank=True)

     def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length = 200,null=True)
    ctc = models.CharField(max_length=200,null=True)
    stipend = models.CharField(max_length=200,null=True)
    hiring_who = models.ManyToManyField(trade)
    Role_offered = models.ManyToManyField(role)  
    company_contact = models.CharField(max_length=200,null=True,blank=True)
    additional_information = models.CharField(max_length=500,null=True,blank=True)
    Spoc = models.ForeignKey(Coordinator,null=True,blank=True,on_delete=models.SET_NULL)
    Manager = models.ForeignKey(Manager,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class CommentSection(models.Model):
    comment = models.TextField() 
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class headplacementcoordinator(models.Model):
    my_user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    
    



