from django.db import models

# Create your models here.

class DumbModel(models.Model):
    text = models.TextField()
    
    def __str__(self): 
        return f"ID {self.pk}: {self.text}"
