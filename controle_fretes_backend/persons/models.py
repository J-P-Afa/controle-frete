from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint
from django.core.exceptions import ValidationError
from .constants import (
    MAX_NAME_LENGTH, MAX_ZIPCODE_LENGTH, validate_min_name, validate_min_street,
    validate_zip_code, validate_number_range, validate_min_length, validate_abbreviation,
    validate_percentage_range, validate_state_name, validate_document_number_numeric,
)


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    address_id = models.ForeignKey('persons.Address', on_delete=models.CASCADE, related_name='person', null=False)
    document_id = models.OneToOneField('persons.Document', on_delete=models.CASCADE, related_name='person', null=False)

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        validators=[validate_min_name],
        error_messages={
            'max_length': f'Name must be at most {MAX_NAME_LENGTH} characters',
        }
    )

    def __str__(self):
        return f'{self.person_id} - {self.name}'


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey('persons.State', on_delete=models.CASCADE, related_name='addresses', null=False)
    delivery_classification_id = models.ForeignKey('persons.DeliveryClassification', on_delete=models.CASCADE, related_name='addresses', null=False)

    street = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        validators=[validate_min_street],
        error_messages={
            'max_length': f'Street must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    number = models.PositiveSmallIntegerField(
        null=False,
        validators=[validate_number_range]
    )
    complement = models.CharField(
        max_length=MAX_NAME_LENGTH,
        default='',
        error_messages={
            'max_length': f'Complement must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    neighborhood = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        error_messages={
            'max_length': f'Neighborhood must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    city = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        error_messages={
            'max_length': f'City must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    zip_code = models.CharField(
        max_length=MAX_ZIPCODE_LENGTH,
        null=False,
        validators=validate_zip_code,
        error_messages={
            'max_length': f'Zip code must be exactly {MAX_ZIPCODE_LENGTH} characters',
        }
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['state_id', 'delivery_classification_id'],
                name='unique_state_delivery_classification'
            ),
            models.CheckConstraint(check=Q(number__gt=0), name='check_number_gt_0'),
            models.CheckConstraint(check=Q(number__lte=99999), name='check_number_lte_99999')
        ]

    def __str__(self):
        return f'{self.address_id} - {self.street}, {self.number} {self.complement}, {self.neighborhood}, {self.city}/{self.state_id.abbreviation}; {self.zip_code}'


class DeliveryClassification(models.Model):
    delivery_classification_id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        validators=[validate_min_length],
        error_messages={
            'max_length': f'Delivery classification must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    default_freight_percentage = models.FloatField(
        null=False,
        validators=[validate_percentage_range]
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(default_freight_percentage__gte=0.001) & Q(default_freight_percentage__lte=0.40),
                name='check_default_freight_percentage_range'
            ),
        ]

    def __str__(self):
        return f'{self.delivery_classification_id} - {self.name}'


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        validators=[validate_state_name],
        error_messages={
            'max_length': f'State name must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    abbreviation = models.CharField(
        max_length=2,
        null=False,
        validators=[validate_abbreviation],
        error_messages={
            'max_length': 'Abbreviation must be exactly 2 characters',
        }
    )

    def __str__(self):
        return f'{self.state_id} - {self.abbreviation}'


class DocumentType(models.Model):
    document_type_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=10,
        null=False,
        validators=[validate_min_length],
        error_messages={
            'max_length': 'Document type name must be at most 10 characters',
        }
    )
    length = models.IntegerField(
        null=False,
        validators=[MinValueValidator(1, message='Length must be at least 1')]
    )

    def __str__(self):
        return f'{self.document_type_id} - {self.name}'


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_type_id = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='documents', null=False)
    document_number = models.CharField(
        max_length=50,
        null=False,
        validators=[validate_document_number_numeric],
        help_text='O número do documento deve ter exatamente o tamanho definido em DocumentType.length.'
    )

    def __str__(self):
        return f'{self.document_id} - {self.document_number}'

    def clean(self):
        super().clean()
        if not self.document_type_id:
            raise ValidationError({
                'document_type_id': 'É necessário escolher um DocumentType antes de validar o número.'
            })

        document_type = self.document_type_id
        expected_length = document_type.length
        actual_length = len(self.document_number or '')

        if actual_length != expected_length:
            raise ValidationError({
                'document_number': (
                    f'O número do documento deve ter exatamente {expected_length} caracteres '
                    f'(atualmente tem {actual_length}).'
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PersonType(models.Model):
    person_type_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        error_messages={
            'max_length': f'Person type name must be at most {MAX_NAME_LENGTH} characters',
        }
    )
    is_transporter = models.BooleanField(default=False)
    is_sender = models.BooleanField(default=False)
    is_receiver = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.person_type_id} - {self.name}'

    def clean(self):
        super().clean()
        if not self.is_transporter and not self.is_sender and not self.is_receiver:
            raise ValidationError({
                'is_transporter': 'At least one of the following fields must be true: is_transporter, is_sender, is_receiver',
                'is_sender': 'At least one of the following fields must be true: is_transporter, is_sender, is_receiver',
                'is_receiver': 'At least one of the following fields must be true: is_transporter, is_sender, is_receiver',
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
