from fastapi.testclient import TestClient

from tests.integration_tests.data.books import (
    valid_book_id_1,
    valid_books_limit_2,
    valid_more_authors_info_minus_quantity,
    valid_create_book,
    response_valid_create_book,
    not_valid_create_book,
    response_not_valid_create_book,
    response_valid_remove_book,
    response_not_valid_remove_book,
)


class TestBook:
    def test_get_book(self, client: TestClient):
        response = client.get("/api/v1/books/1")
        data = response.json()
        assert response.status_code == 200
        assert data == valid_book_id_1

    def test_get_books(self, client: TestClient):
        response = client.get("/api/v1/books?limit=2&?offset=0")
        data = response.json()
        assert response.status_code == 200
        assert data == valid_books_limit_2

    def test_get_authors_info(self, client: TestClient):
        response = client.get("/api/v1/books/more/authors?sort=-quantity-books")
        data = response.json()
        assert response.status_code == 200
        assert data == valid_more_authors_info_minus_quantity

    def test_create_book(self, client: TestClient):
        response = client.post(
            "/api/v1/books",
            json=valid_create_book,
        )
        data = response.json()
        assert response.status_code == 201
        assert data == response_valid_create_book

    def test_create_book_not_valid(self, client: TestClient):
        response = client.post(
            "/api/v1/books",
            json=not_valid_create_book,
        )
        data = response.json()
        assert response.status_code == 404
        assert data == response_not_valid_create_book

    def test_remove_book(self, client: TestClient):
        response = client.delete("/api/v1/books/8")
        data = response.json()
        assert response.status_code == 200
        assert data == response_valid_remove_book

    def test_remove_book_not_valid(self, client: TestClient):
        response = client.delete("/api/v1/books/99999")
        data = response.json()
        assert response.status_code == 404
        assert data == response_not_valid_remove_book
