from decimal import Decimal
from enum import Enum


def empty_string(field_name: str) -> str:
    return f'{field_name} не может быть пустым или содержать пробелы'


def invalid_string(field_name: str, value: str) -> str:
    return f'{field_name} не корректные данные: "{value}"'


def round_decimal(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))


class GroupFields(str, Enum):
    field_1 = "id"
    field_2 = "-id"
    field_3 = "avg-price"
    field_4 = "-avg-price"
    field_5 = "quantity-books"
    field_6 = "-quantity-books"
