from src.dtos.user import UserDTO
from src.models.user import User


def create_user(user: UserDTO) -> str:
    userDocument = User(
        email=user.email,
        flatNumber=user.flatNumber,
        hashedPass=user.hashedPass,
        isAdmin=user.isAdmin,
    )

    userDocument.save()

    return str(userDocument.id)


def getUserByUserId(userId: str) -> UserDTO:
    userDocument: User = User.objects.get(userId=userId, deleted=False)
    return userDocument.toDTO()


def getUserByFlatNumber(flatNumber: str) -> UserDTO:
    userDocument: User = User.objects.get(flatNumber=flatNumber, deleted=False)
    return userDocument.toDTO()


def getUserIdByFlatNumber(flatNumber: str) -> str:
    userDocument: User = User.objects.get(flatNumber=flatNumber, deleted=False)
    return str(userDocument.id)


def get_or_none_user_by_flat_number(flatNumber: str) -> UserDTO | None:
    userDocument: User | None = User.objects.filter(flatNumber=flatNumber).first()
    return userDocument.toDTO() if userDocument else None
