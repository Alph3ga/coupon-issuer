from src.dtos.user import UserDTO
from src.models.user import User


def create_user(user: UserDTO) -> None:
    userDocument = User(
        userId=user.userId,
        name=user.name,
        phoneNumber=user.phoneNumber,
        flatNumber=user.flatNumber,
        hashedPass=user.hashedPass,
        isAdmin=user.isAdmin,
    )

    userDocument.save()


def getUserByUserId(userId: str) -> UserDTO:
    userDocument: User = User.objects.get(userId=userId, deleted=False)
    return userDocument.toDTO()


def getUserByFlatNumber(flatNumber: str) -> UserDTO:
    userDocument: User = User.objects.get(flatNumber=flatNumber, deleted=False)
    return userDocument.toDTO()
