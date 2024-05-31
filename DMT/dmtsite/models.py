from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class userTransaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    visited_page = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time} - {self.visited_page}"
