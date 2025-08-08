from src.dtos.user_verification_status import UserVerificationStatusDTO
from src.models.user_verification_status import UserVerificationStatusUpdate


def create_user_verification_status_update(
    dto: UserVerificationStatusDTO,
) -> UserVerificationStatusUpdate:
    model = UserVerificationStatusUpdate.from_dto(dto)
    model.save()
    return model


def get_all_status_update(user_id: str) -> list[UserVerificationStatusDTO]:
    updates: list[UserVerificationStatusUpdate] = (
        UserVerificationStatusUpdate.objects(user=user_id).order_by("-updatedOn").all()
    )
    return [update.to_dto() for update in updates]


def get_latest_status_update(user_id: str) -> UserVerificationStatusDTO:
    update: UserVerificationStatusUpdate | None = (
        UserVerificationStatusUpdate.objects(user=user_id).order_by("-updatedOn").first()
    )
    if not update:
        raise ValueError(f"No verification status found for user {user_id}")
    return update.to_dto()
