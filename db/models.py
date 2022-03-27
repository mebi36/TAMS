from django.db import models
from manage import init_django

init_django()

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, null=True, blank=True)
    level_of_study = models.IntegerField(null=True, blank=True)
    fingerprint_template = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reg_number})"

