from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Shipment, ShipmentInvoice


@receiver(pre_save, sender=Shipment)
def calculate_shipment_km_total(sender, instance, **kwargs):
    instance.total_km = instance.end_km - instance.start_km


@receiver(pre_save, sender=ShipmentInvoice)
def calculate_shipment_invoice_totals(sender, instance, **kwargs):
    instance.loaded_ton_total_price = instance.loaded_ton_unit_price * instance.loaded_ton_quantity
    instance.unloaded_ton_total_price = instance.unloaded_ton_unit_price * instance.unloaded_ton_quantity
    instance.delivery_total_price = instance.delivery_unit_price * instance.delivery_quantity
    instance.extra_hour_total_price = instance.extra_hour_unit_price * instance.extra_hour_quantity
    
    instance.invoice_freight_total_price = (
        instance.loaded_ton_total_price +
        instance.unloaded_ton_total_price +
        instance.delivery_total_price +
        instance.extra_hour_total_price
    ) 