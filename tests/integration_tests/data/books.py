add_books = [
    {"title": "Тень ветра", "price": 1200, "quantity": 5, "author_id": 1},
    {"title": "Золотой путь", "price": 800, "quantity": 2, "author_id": 1},
    {"title": "Белые ночи", "price": 950, "quantity": 0, "author_id": 2},
    {"title": "Глубина разума", "price": 1500, "quantity": 3, "author_id": 2},
    {"title": "Сквозь время", "price": 2000, "quantity": 1, "author_id": 2},
    {"title": "Остров", "price": 1300, "quantity": 6, "author_id": 1},
    {"title": "Порт", "price": 1100, "quantity": 7, "author_id": 1}
]

valid_create_book = {
    'title': 'Тест книга',
    'price': 300,
    'quantity': 20,
    'author_id': 1
}
response_valid_create_book = {
    'id': 8,
    'title': 'Тест книга',
    'price': '300.00',
    'quantity': 20,
    'author': {'id': 1, 'name': 'Пушкин'},
}

not_valid_create_book = {
    'title': 'Тест книга',
    'price': 300,
    'quantity': 20,
    'author_id': 99999
}
response_not_valid_create_book = {'detail': 'Не существует объекта по данному атрибуту: author_id=99999'}

valid_book_id_1 = {
    'author': {'id': 1, 'name': 'Пушкин'},
    'id': 1,
    'price': '1200.00',
    'quantity': 5,
    'title': 'Тень ветра'
}

valid_books_limit_2 = [
    {
        'author': {'id': 1, 'name': 'Пушкин'},
        'id': 1,
        'price': '1200.00',
        'quantity': 5,
        'title': 'Тень ветра'
    },
    {
        'author': {'id': 1, 'name': 'Пушкин'},
        'id': 2,
        'price': '800.00',
        'quantity': 2,
        'title': 'Золотой путь'
    }
]

valid_more_authors_info_minus_quantity = [
    {'avg_price': 1100, 'id': 1, 'name': 'Пушкин', 'quantity_books': 4},
    {'avg_price': 1483, 'id': 2, 'name': 'Толстой', 'quantity_books': 3}
]

response_valid_remove_book = {'deleted': 'объект book_id=8 удалён успешно'}
response_not_valid_remove_book = {'detail': 'Не существует объекта по данному атрибуту: book_id=99999'}
