from django.db import models


class LoadMovementType(models.Model):
    load_movement_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False)


class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    truck_id = models.ForeignKey('trucks.Truck', on_delete=models.CASCADE)
    shipment_closing_id = models.ForeignKey('shipments.ShipmentClosing', on_delete=models.CASCADE)

    start_km = models.FloatField(null=False)
    end_km = models.FloatField(null=False)
    km_total = models.FloatField(null=False)
    km_value = models.FloatField(null=False)
    fixed_cost = models.FloatField(default=0.0)


class ShipmentInvoice(models.Model):
    shipment_invoice_id = models.AutoField(primary_key=True)
    shipment_id = models.ForeignKey('shipments.Shipment', on_delete=models.CASCADE)
    invoice_id = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE)
    loaded_movement_type_id = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE, related_name='loaded_shipments')
    unloaded_movement_type_id = models.ForeignKey('shipments.LoadMovementType', on_delete=models.CASCADE, related_name='unloaded_shipments')

    loaded_ton_unit_price = models.FloatField(null=False)
    loaded_ton_quantity = models.FloatField(null=False)
    loaded_ton_total_price = models.FloatField(null=False)

    unloaded_ton_unit_price = models.FloatField(null=False)
    unloaded_ton_quantity = models.FloatField(null=False)
    unloaded_ton_total_price = models.FloatField(null=False)

    delivery_unit_price = models.FloatField(null=False)
    delivery_quantity = models.FloatField(null=False)   
    delivery_total_price = models.FloatField(null=False)

    extra_hour_unit_price = models.FloatField(default=0.0)
    extra_hour_quantity = models.IntegerField(null=False, default=0)
    extra_hour_total_price = models.FloatField(default=0.0)
    
    invoice_freight_total_price = models.FloatField(null=False)


class ShipmentClosing(models.Model):
    shipment_closing_id = models.AutoField(primary_key=True)
    
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    sequence = models.IntegerField(null=False)
