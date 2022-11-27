from django.db import models

class MyUser(models.Model):
    username =          models.CharField(max_length=255, unique=True)
    password =          models.CharField(max_length=250)
    is_logged_in =      models.BooleanField(default=False)
    is_active =         models.BooleanField(default=True)
    login_token =       models.CharField(max_length=500, null=True, blank=True)
    access_token =      models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.username

class Item(models.Model):
    item_id = models.CharField(max_length=100)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100)