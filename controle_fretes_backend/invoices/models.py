from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey('persons.Person', on_delete=models.CASCADE, related_name='sender_invoices', null=False)
    receiver_id = models.ForeignKey('persons.Person', on_delete=models.CASCADE, related_name='receiver_invoices', null=False)
    transporter_id = models.ForeignKey('persons.Person', on_delete=models.CASCADE, related_name='transporter_invoices', null=False)
 
    invoice_number = models.CharField(
        max_length=9,
        null=False,
        validators=[
            MinLengthValidator(1, message='Invoice number must be at least 1 digit'),
            MaxLengthValidator(9, message='Invoice number must be at most 9 digits'), 
            RegexValidator(
                regex=r'^\d{1,9}$',
                message='Invoice number must be only numerical digits',
                code='invalid_invoice_number'
            )
        ]
    )
    invoice_series = models.CharField(
        max_length=3,
        null=False,
        validators=[
            MinLengthValidator(1, message='Invoice series must be at least 1 digit'),
            MaxLengthValidator(3, message='Invoice series must be at most 3 digits'),
            RegexValidator(
                regex=r'^\d{1,3}$',
                message='Invoice series must be only numerical digits',
                code='invalid_invoice_series'
            )
        ]
    )
    invoice_key = models.CharField(
        max_length=44,
        null=False,
        validators=[
            MinLengthValidator(44),
            MaxLengthValidator(44),
            RegexValidator(
                regex=r'^\d{44}$',
                message='Invoice key must be exactly 44 numerical digits',
                code='invalid_invoice_key'
            )
        ]
    )
    issue_date = models.DateField(
        null=False,
        validators=[
            MinValueValidator(limit_value=date(2000, 1, 1), message='Issue date must be at least 2000-01-01'),
            MaxValueValidator(limit_value=date.today, message='Issue date cannot be in the future')
        ]
    )
    total_value = models.FloatField(
        null=False,
        validators=[
            MinValueValidator(0.01, message='Total value must be greater than zero'),
            MaxValueValidator(limit_value=1000000.00, message='Total value must be less than 1,000,000')
        ]
    )
    gross_weight = models.FloatField(
        null=False,
        validators=[
            MinValueValidator(0.01, message='Gross weight must be greater than zero'),
            MaxValueValidator(limit_value=50000.00, message='Gross weight must be less than 50,000')
        ]
    )



class ShipmentInvoice(models.Model):
    shipment_invoice_id = models.AutoField(primary_key=True)
    shipment_id = models.ForeignKey('shipments.Shipment', on_delete=models.CASCADE, related_name='shipment_invoices', null=False)

    shipment_invoice_number = models.CharField(
        max_length=9,
        null=False,
        validators=[
            MinLengthValidator(1, message='Shipment invoice number must be at least 1 digit'),
            MaxLengthValidator(9, message='Shipment invoice number must be at most 9 digits'),
        ]
    )
    shipment_invoice_series = models.CharField(
        max_length=3,
        null=False,
        validators=[
            MinLengthValidator(1, message='Shipment invoice series must be at least 1 digit'),
            MaxLengthValidator(3, message='Shipment invoice series must be at most 3 digits'),
        ]
    )
    shipment_invoice_key = models.CharField(
        max_length=44,
        null=False,
        validators=[
            MinLengthValidator(44),
            MaxLengthValidator(44),
        ]
    )

    total_value = models.FloatField(
        null=False,
        validators=[
            MinValueValidator(0.01, message='Total value must be greater than zero'),
            MaxValueValidator(limit_value=1000000.00, message='Total value must be less than 1,000,000')
        ]
    )
    total_weight = models.FloatField(
        null=False,
        validators=[
            MinValueValidator(0.01, message='Total weight must be greater than zero'),
            MaxValueValidator(limit_value=50000.00, message='Total weight must be less than 50,000')
        ]
    )
