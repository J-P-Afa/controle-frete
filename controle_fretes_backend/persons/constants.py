from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


MAX_NAME_LENGTH = 255
MAX_ZIPCODE_LENGTH = 8

validate_min_name = MinLengthValidator(3, message='Name must be at least 3 characters long')
validate_min_street = MinLengthValidator(3, message='Street must be at least 3 characters long')
validate_min_length = MinLengthValidator(3, message='This field must be at least 3 characters long')


validate_abbreviation = RegexValidator(
    regex=r'^[A-Z]{2}$',
    message='Abbreviation must be exactly two uppercase letters'
)


validate_zip_code = [
    RegexValidator(
        regex=r'^\d{8}$',
        message='Zip code must be exactly 8 digits'
    )
]


def validate_number_range(value):
    if value <= 0:
        raise ValidationError('Number must be greater than 0')
    if value > 99999:
        raise ValidationError('Number must be less than or equal to 99999')


def validate_percentage_range(value):
    if not (0.001 <= value <= 0.40):
        raise ValidationError('Freight percentage must be between 0.001 and 0.40')


def validate_state_name(value):
    if not value.istitle():
        raise ValidationError('State name must start with uppercase and be properly capitalized')


def validate_document_number_numeric(value):
    if not value.isdigit():
        raise ValidationError('Document number must contain only digits')
