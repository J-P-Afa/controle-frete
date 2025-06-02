from .models import Shipment, ShipmentInvoice


class ShipmentService:
    @staticmethod
    def calculate_km_total(start_km: float, end_km: float) -> float:
        return end_km - start_km

    @staticmethod
    def create_shipment(data: dict) -> Shipment:
        shipment = Shipment(**data)
        shipment.km_total = ShipmentService.calculate_km_total(shipment.start_km, shipment.end_km)
        shipment.save()
        return shipment


class ShipmentInvoiceService:
    @staticmethod
    def calculate_totals(unit_prices: dict, quantities: dict) -> dict:
        loaded_total = unit_prices['loaded_ton_unit_price'] * quantities['loaded_ton_quantity']
        unloaded_total = unit_prices['unloaded_ton_unit_price'] * quantities['unloaded_ton_quantity']
        delivery_total = unit_prices['delivery_unit_price'] * quantities['delivery_quantity']
        extra_hour_total = unit_prices['extra_hour_unit_price'] * quantities['extra_hour_quantity']

        return {
            'loaded_ton_total_price': loaded_total,
            'unloaded_ton_total_price': unloaded_total,
            'delivery_total_price': delivery_total,
            'extra_hour_total_price': extra_hour_total,
            'invoice_freight_total_price': loaded_total + unloaded_total + delivery_total + extra_hour_total
        }

    @staticmethod
    def create_shipment_invoice(data: dict) -> ShipmentInvoice:
        quantities = {
            'loaded_ton_quantity': data['loaded_ton_quantity'],
            'unloaded_ton_quantity': data['unloaded_ton_quantity'],
            'delivery_quantity': data['delivery_quantity'],
            'extra_hour_quantity': data['extra_hour_quantity']
        }
        
        totals = ShipmentInvoiceService.calculate_totals(
            {k: data[k] for k in ['loaded_ton_unit_price', 'unloaded_ton_unit_price', 'delivery_unit_price', 'extra_hour_unit_price']},
            quantities
        )
        
        data.update(totals)    
        
        invoice = ShipmentInvoice(**data)
        invoice.save()
        return invoice
    
