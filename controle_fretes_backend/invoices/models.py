from django.db import models


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10, null=False)
    key = models.CharField(max_length=44)
    date = models.DateField(null=False)
    value = models.FloatField(null=False)
    gross_weight = models.FloatField(null=False)
