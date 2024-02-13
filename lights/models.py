from django.db import models

# Create your models here.
class Light(models.Model):
    bulb_ip = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    status = models.BooleanField(null=True)

    def __str__(self):
        return self.title