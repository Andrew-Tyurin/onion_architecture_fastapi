from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        try:
            columns = self.__table__.columns.keys()
        except AttributeError:
            # Если __table__ ещё нет (объект только создан)
            return f'<{self.__class__.__name__}: __table__ - отсутствует>'

        values = (f"{col}={getattr(self, col, 'Ошибка')}" for col in columns)
        return f'<{self.__class__.__name__}: {"; ".join(values)}>'
