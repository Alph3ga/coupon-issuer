from pydantic import BaseModel


class SignupBody(BaseModel):
    flat_number: str
    email: str | None
    password: str | None


class TokenResponse(BaseModel):
    token_type: str
    access_token: str


class LoginBody(BaseModel):
    flat_number: str
    password: str | None
