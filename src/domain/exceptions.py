# src/domain/exceptions.py


class DomainError(Exception):
    """Classe de base pour toutes les exceptions du domaine."""

    pass


class UserNotFoundError(DomainError):
    """Exception levée lorsqu'un utilisateur n'est pas trouvé."""

    pass


class ValidationError(DomainError):
    """Exception levée lorsque les données ne sont pas valides."""

    pass
