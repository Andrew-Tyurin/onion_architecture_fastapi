from fastapi.testclient import TestClient


class TestAuthor:
    def test_get_authors(self, client: TestClient):
        response = client.get(f"/api/v1/books/authors")
        data = response.json()
        assert response.status_code == 200
        assert data == [
            {'id': 1, 'name': 'Пушкин'},
            {'id': 2, 'name': 'Толстой'}
        ]

    def test_create_author(self, client: TestClient):
        response = client.post(
            f"/api/v1/books/authors",
            json={"name": "тЕсТ"}
        )
        data = response.json()
        assert response.status_code == 201
        assert data == {"id": 3, "name": "Тест"}

    def test_create_author_not_valid(self, client: TestClient):
        response = client.post(
            f"/api/v1/books/authors",
            json={"name": "Имя1"}
        )
        data = response.json()
        assert response.status_code == 422
        assert data['detail'][0]['msg'] == 'Value error, name не корректные данные: "Имя1"'

    def test_remove_author(self, client: TestClient):
        response = client.delete(f"/api/v1/books/authors/3")
        data = response.json()
        assert response.status_code == 200
        assert data == {'deleted': 'объект author_id=3 удалён успешно'}

    def test_remove_author_not_valid(self, client: TestClient):
        response = client.delete(f"/api/v1/books/authors/999999")
        data = response.json()
        assert response.status_code == 404
        assert data == {'detail': 'Не существует объекта по данному атрибуту: author_id=999999'}
