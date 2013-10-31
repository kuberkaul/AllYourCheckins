from django.db import models
from datetime import datetime
# Create your models here.

class savedTimelines(models.Model):
    userId = models.CharField(max_length=30)
    image_encodedString = models.TextField()
    
