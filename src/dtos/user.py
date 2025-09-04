from pydantic import BaseModel


class UserDTO(BaseModel):
    email: str | None
    flatNumber: str
    hashedPass: bytes | None
    isAdmin: bool
