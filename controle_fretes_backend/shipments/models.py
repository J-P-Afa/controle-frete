from os import name
from django.db import models


class LoadMovementType(models.Model):
    load_movement_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False)


class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    truck_id = models.ForeignKey('trucks.Truck', on_delete=models.CASCADE)
    shipment_closing_id = models.ForeignKey('shipments.ShipmentClosing', on_delete=models.CASCADE)

    start_km = models.IntegerField(null=False)
    end_km = models.IntegerField(null=False)
    km_value = models.FloatField(null=False)
    fixed_cost = models.FloatField(default=0.0)


class ShipmentInvoice(models.Model):
    shipment_invoice_id = models.AutoField(primary_key=True)
    shipment_id = models.ForeignKey('shipments.Shipment', on_delete=models.CASCADE)
    invoice_id = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE)
    load_movement_type_id_loaded = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE)
    load_movement_type_id_unloaded = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE)

    loaded_weight_price = models.FloatField(null=False)
    unloaded_weight_price = models.FloatField(null=False)
    delivery_price = models.FloatField(null=False)
    extra_hour_quantity = models.IntegerField(null=False, default=0)
    extra_hour_price = models.FloatField(default=0.0)
    extra_unload_price = models.FloatField(default=0.0)
    


class ShipmentClosing(models.Model):
    shipment_closing_id = models.AutoField(primary_key=True)
    
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    sequence = models.IntegerField(null=False)
