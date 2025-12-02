from django.db import models

class Trip(models.Model):
    """
    Represents a booked trip in the database.
    """
    trip_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.trip_id}"

