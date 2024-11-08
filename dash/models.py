from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Nature(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category)


class Job_Listing(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=50)
    nature = models.ForeignKey(Nature, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now=True)
    payment = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="pending")
    tasker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="short_tasker")

    def __str__(self):
        return str(self.job)


class Feedback(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job_Listing, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.body)
    

class Job_Proposal(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='test@email.com')
    job = models.ForeignKey(Job_Listing, on_delete=models.SET_NULL, null=True)
    website = models.CharField(max_length=200)
    application = models.TextField()
    create_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="sent")
    nature = models.CharField(max_length=50, default="Short Task")

    def __str__(self):
        return str(self.job)
