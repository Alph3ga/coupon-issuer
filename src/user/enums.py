from enum import StrEnum, auto


class UserVerificationStatus(StrEnum):
    APPROVED = auto()
    PENDING = auto()
    REJECTED = auto()
