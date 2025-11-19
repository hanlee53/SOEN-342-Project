from django.db import models

class Client(models.Model):
    """
    Stores the record of a traveller in the database.
    """
    client_id = models.CharField(max_length=50, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.client_id})"

