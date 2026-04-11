import secrets

from fastapi import HTTPException

from infrastructure.db.base import Base


def is_obj(obj: Base | None, param: str | int) -> None:
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=f"Не существует объекта по данному атрибуту: {param}",
        )


class CustomCsrfToken:
    """
    Шаблон реализации, работы с CSRF.
    В дальнейшем нужно использовать redis...
    (возможно)
    """
    tokens: set = set()

    @property
    def create_token(self) -> str:
        """рандомная строка из разных символов"""
        return secrets.token_urlsafe(16)


CsrfToken = CustomCsrfToken()
