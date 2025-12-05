from django.db import models

class Trip(models.Model):
    """
    Represents a booked trip in the database.
    """
    trip_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='trips', null=True) # Allow null for now or legacy
    source_city = models.CharField(max_length=100, default="Unknown")
    destination_city = models.CharField(max_length=100, default="Unknown")
    date = models.DateField(default="2025-01-01")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Store connections as a description string for simplicity in this iteration
    route_description = models.TextField(help_text="Description of the route structure", default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        client_str = str(self.client) if self.client else "Unknown Client"
        return f"Trip {self.trip_id} for {client_str}"

