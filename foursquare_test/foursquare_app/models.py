from django.db import models
from datetime import datetime
# Create your models here.

class photourl(models.Model):
    url = models.CharField(max_length = 128)
    uploaded = models.DateTimeField()

    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)
