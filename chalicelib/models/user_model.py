
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from chalicelib.validators import user_validators


class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50, description="Unique username (alphanumeric and underscores)")
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="Hashed password (not returned in responses)")
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        return user_validators.UserValidator.validate_username(v)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        return user_validators.UserValidator.validate_password(v)


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100, description="Password (must contain letters and numbers)")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        return user_validators.UserValidator.validate_username(v)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        return user_validators.UserValidator.validate_password_required(v)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")

    @field_validator('username', 'password')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        return user_validators.UserValidator.validate_not_empty(v)
