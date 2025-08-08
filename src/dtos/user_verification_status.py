from datetime import datetime

from pydantic import BaseModel

from src.user.enums import UserVerificationStatus


class UserVerificationStatusUpdateDTO(BaseModel):
    user: str  # user ID as string
    status: UserVerificationStatus
    updatedOn: datetime
    updatedBy: datetime | None = None
    isAdminUpdate: bool = False
