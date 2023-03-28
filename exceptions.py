class TokenNotFoundException(Exception):
    """Обработка исключения при отсуствии хотя бы одного из токенов."""

    pass


class EndPointIsNotAvailiable(Exception):
    """Обработка исключения при недоступности ENDPOINT API."""

    pass
