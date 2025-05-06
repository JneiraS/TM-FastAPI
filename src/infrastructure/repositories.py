from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional

from src.application.use_cases import UserRepository
from src.domain.models import User
from src.domain.exceptions import UserNotFoundError
from src.infrastructure.sqlalchemy_models import UserModel
from src.services.user_services import new_user_services
from src.infrastructure.persistence.db import engine, get_db

# Create a sessionmaker bound to your engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class UserMapper:
    """
    Classe responsable de la conversion entre les objets de domaine User
    et les modèles d'infrastructure UserModel.
    """

    @staticmethod
    def to_domain(user_model) -> Optional[User]:
        """
        Convertit un modèle de base de données en objet du domaine.
        """
        if not user_model:
            return None
        return User(
            id=user_model.id,
            name=user_model.name,
            assigned_tasks=user_model.assigned_tasks,
        )

    @staticmethod
    def to_infrastructure(user: User) -> UserModel:
        """
        Convertit un objet du domaine en modèle de base de données.
        """
        return UserModel(
            id=user.id,
            name=user.name,
            assigned_tasks=user.assigned_tasks,
        )


class SQLAlchemyUserRepository(UserRepository):
    """
    Implémentation du UserRepository utilisant SQLAlchemy comme ORM.
    Cette classe gère la persistance des utilisateurs.
    """

    def __init__(self, session: Session):
        """
        Initialise le repository avec une session de base de données.
        """
        self.session = session

    def save(self, user: User) -> None:
        """
        Enregistre un nouvel utilisateur dans la base de données.
        """
        if not user.name or len(user.name.strip()) == 0:
            raise ValueError("User name ne peut pas être vide.")

        user_model = UserModel(name=user.name)
        self.session.add(user_model)
        self.session.commit()
        user.id = user_model.id

    def get_all(self) -> List[User]:
        """
        Récupère tous les utilisateurs de la base de données.

        """
        user_models = self.session.query(UserModel).all()
        return [UserMapper.to_domain(user_model) for user_model in user_models]

    def get_by_id(self, user_id: int) -> User:
        """
        Récupère un utilisateur par son identifiant.
        """
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        if not user_model:
            raise UserNotFoundError(f"L'utilisateur avec l'id {user_id} a été trouvé.")
        return UserMapper.to_domain(user_model)

    def get_by_name(self, name: str) -> User:
        """
        Récupère un utilisateur par son nom.
        UserNotFoundError: Si aucun utilisateur n'est trouvé avec ce nom
        """
        if not name or len(name.strip()) == 0:
            raise ValueError("User name ne peut pas être vide")

        user_model = self.session.query(UserModel).filter_by(name=name).first()
        if not user_model:
            raise UserNotFoundError(f"Aucun User avec le nom: '{name}' a été trouvé.")
        return UserMapper.to_domain(user_model)

    def update(self, user: User) -> User:
        """
        Met à jour un utilisateur existant.
        """
        if not user.id:
            raise ValueError("User ID est requis pour la mise à jour")

        if not user.name or len(user.name.strip()) == 0:
            raise ValueError("User name ne peut pas être vide")

        user_model = self.session.query(UserModel).filter_by(id=user.id).first()
        if not user_model:
            raise UserNotFoundError(f"User avec l'id {user.id} n'a pas été trouvé.")

        user_model.name = user.name
        self.session.commit()
        return UserMapper.to_domain(user_model)

    def delete(self, user_id: int) -> bool:
        """
        Supprime un utilisateur par son identifiant.
        """
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        if not user_model:
            raise UserNotFoundError(f"User avec l'id {user_id} n'a pas été trouvé.")

        self.session.delete(user_model)
        self.session.commit()
        return True


def get_user_service(db: Session = Depends(get_db)):
    """
    Crée et retourne un service utilisateur avec ses dépendances.
    À utiliser comme dépendance dans les endpoints FastAPI.
    """
    user_repo = SQLAlchemyUserRepository(db)
    return new_user_services(user_repo)
