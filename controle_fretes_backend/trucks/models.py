from django.db import models


class Truck(models.Model):
    truck_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False)
    km_value = models.FloatField(null=False)
    fixed_cost = models.FloatField(default=0.0)
