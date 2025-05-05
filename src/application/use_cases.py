"""
Classe de base abstraite définissant l'interface du référentiel pour les opérations utilisateur.

Cette classe définit le contrat pour les opérations d'accès aux données utilisateur, notamment :
— Créer : Sauvegarder un nouvel utilisateur
— Lire : Récupérer des utilisateurs selon différents critères
— Mettre à jour : Modifier les informations d'un utilisateur existant
— Supprimer : Retirer un utilisateur du référentiel.

Les sous-classes doivent implémenter toutes les méthodes abstraites pour fournir une logique d'accès aux données concrète."""

from src.domain.models import User
from abc import ABC, abstractmethod

class UserRepository(ABC):

    #Create

    @abstractmethod
    def save(self, user: User):
        pass

    # Read
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def get_by_name(self, name: str):
        pass

    #Update
    @abstractmethod
    def update(self, user: User):
        pass

    #Delete
    @abstractmethod
    def delete(self, user_id: int):
        pass


