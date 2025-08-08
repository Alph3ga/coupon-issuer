from pydantic import BaseModel


class UserDTO(BaseModel):
    userId: str
    name: str
    phoneNumber: str | None = None
    flatNumber: str
    hashedPass: bytes
    isAdmin: bool
