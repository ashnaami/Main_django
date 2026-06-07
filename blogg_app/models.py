from django.db import models

# Create your models here.
class TB_User(models.Model):
    name = models.CharField(max_length=25,default="")
    phone = models.CharField(max_length=10,default="")
    email=models.EmailField(max_length=20,default="")
    password = models.CharField(max_length=15, default="")

class TB_Post(models.Model):
    user = models.ForeignKey('TB_User',on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=5000, default="")
    category = models.CharField(max_length=25,default="")
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

class TB_Comments(models.Model):
    user = models.ForeignKey('TB_User',on_delete=models.CASCADE,blank=True,null=True)
    post = models.ForeignKey('TB_Post',on_delete=models.CASCADE,blank=True,null=True)
    comments = models.CharField(max_length=50,default="")

class TB_Like(models.Model):
    user = models.ForeignKey('TB_User',on_delete=models.CASCADE,blank=True,null=True)
    post = models.ForeignKey('TB_Post',on_delete=models.CASCADE,blank=True,null=True)
