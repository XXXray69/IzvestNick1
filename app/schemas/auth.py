from typing import Optional
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    phone_prefix: str = Field(default='+7', max_length=12)
    phone_number: str = Field(min_length=5, max_length=32)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)


class CompleteProfileRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    phone_number: str
    password: str
    device_name: Optional[str] = None


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
