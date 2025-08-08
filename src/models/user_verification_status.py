from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EnumField,
    ReferenceField,
    StringField,
)

from src.dtos.user_verification_status import UserVerificationStatusUpdateDTO
from src.models.user import User
from src.models.user_verification_status import UserVerificationStatusUpdate
from src.user.enums import UserVerificationStatus as UserVerificationStatus


class UserVerificationStatusUpdate(Document):
    meta = {"indexes": ["user", "-updatedOn"]}
    user = ReferenceField(User, required=True)
    status = EnumField(UserVerificationStatus, use_value=True, required=True)
    updatedOn = DateTimeField(default=datetime.utcnow)
    updatedBy = StringField()
    isAdminUpdate = BooleanField(default=False)

    def to_dto(self) -> UserVerificationStatusUpdateDTO:
        return UserVerificationStatusUpdateDTO(
            user=str(self.user.id),
            status=self.status,
            updatedOn=self.updatedOn,
            updatedBy=self.updatedBy,
            isAdminUpdate=self.isAdminUpdate,
        )

    @classmethod
    def from_dto(cls, dto: UserVerificationStatusUpdateDTO) -> UserVerificationStatusUpdate:
        user_ref = User.objects.get(id=dto.user)  # Throws DoesNotExist if not found
        return cls(
            user=user_ref,
            status=dto.status,
            updatedOn=dto.updatedOn,
            updatedBy=dto.updatedBy,
            isAdminUpdate=dto.isAdminUpdate,
        )
