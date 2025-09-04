from datetime import datetime

from mongoengine import BinaryField, BooleanField, DateTimeField, Document, StringField

from src.dtos.user import UserDTO


class User(Document):
    meta = {"indexes": [{"fields": ["flatNumber", "deleted"]}]}
    flatNumber = StringField(required=True)
    email = StringField()
    hashedPass = BinaryField()
    isAdmin = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.utcnow)
    deleted = BooleanField(default=False)

    def toDTO(self) -> UserDTO:
        return UserDTO(
            flatNumber=self.flatNumber,
            email=self.email,
            hashedPass=self.hashedPass,
            isAdmin=self.isAdmin,
        )
