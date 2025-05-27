from django.db import models
from django.utils import timezone


class TruckPrices(models.Model):
    truck_prices_id = models.AutoField(primary_key=True)
    truck_id = models.ForeignKey('trucks.Truck', on_delete=models.CASCADE)
    km_value = models.FloatField(null=False)
    fixed_cost = models.FloatField(default=0.0)


class DeliveryPrice(models.Model):
    price = models.FloatField(null=False)


class LoadedWeightPrices(models.Model):
    loaded_weight_prices_id = models.AutoField(primary_key=True)
    load_movement_type_id = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE)
    price = models.FloatField(null=False)


class UnloadedWeightPrices(models.Model):
    unloaded_weight_prices_id = models.AutoField(primary_key=True)
    load_movement_type_id = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE)
    price = models.FloatField(null=False)


class ExtraHourPrice(models.Model):
    price = models.FloatField(null=False)
