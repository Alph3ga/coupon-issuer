from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    email: str | None
    flatNumber: str
    hashedPass: bytes | None
    isAdmin: bool
