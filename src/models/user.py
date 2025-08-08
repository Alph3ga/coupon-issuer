from datetime import datetime

from mongoengine import BinaryField, BooleanField, DateTimeField, Document, StringField

from src.dtos.user import UserDTO


class User(Document):
    meta = {"indexes": [{"fields": ["userId", "deleted"]}, {"fields": ["flatNumber", "deleted"]}]}
    userId = StringField(required=True, unique=True)
    name = StringField(required=True)
    phoneNumber = StringField()
    flatNumber = StringField(required=True)
    hashedPass = BinaryField(required=True)
    isAdmin = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.utcnow)
    deleted = BooleanField(default=False)

    def toDTO(self) -> UserDTO:
        return UserDTO(
            userId=self.userId,
            name=self.name,
            phoneNumber=self.phoneNumber,
            flatNumber=self.flatNumber,
            hashedPass=self.hashedPass,
            isAdmin=self.isAdmin,
        )
