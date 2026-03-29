from fastapi import HTTPException

from infrastructure.db.base import Base


def is_obj(obj: Base | None, param: str | int) -> None:
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=f"Не существует объекта по данному атрибуту: {param}",
        )
