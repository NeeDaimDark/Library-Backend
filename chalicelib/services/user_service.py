
from typing import Dict, Optional, Any, Tuple
from chalicelib.repositories.user_repository import UserRepository
from chalicelib.models import user_model
from chalicelib.utils.exceptions import (
    ValidationException,
    AuthenticationException,
    ConflictException
)
from chalicelib.constants.api import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_TOKEN_EXPIRATION_HOURS,
    ERROR_INVALID_CREDENTIALS,
    ERROR_USERNAME_EXISTS,
    ERROR_UNAUTHORIZED,
    SUCCESS_USER_REGISTERED,
    SUCCESS_LOGIN
)
from pydantic import ValidationError
import jwt
import datetime
import os
import bcrypt


class UserService:

    SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', JWT_SECRET_KEY)
    ALGORITHM: str = JWT_ALGORITHM
    TOKEN_EXPIRATION_HOURS: int = JWT_TOKEN_EXPIRATION_HOURS

    @staticmethod
    def _format_validation_errors(validation_error: ValidationError) -> list:
        errors: list = []
        for error in validation_error.errors():
            errors.append({
                'field': '.'.join(str(loc) for loc in error['loc']),
                'message': error['msg'],
                'type': error['type']
            })
        return errors

    @staticmethod
    def _hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    @staticmethod
    def _generate_token(user_id: int, username: str) -> str:
        payload: Dict[str, Any] = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=UserService.TOKEN_EXPIRATION_HOURS),
            'iat': datetime.datetime.utcnow()
        }
        token: str = jwt.encode(payload, UserService.SECRET_KEY, algorithm=UserService.ALGORITHM)
        return token

    @staticmethod
    def register(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            user_data: user_model.UserRegister = user_model.UserRegister(**data)

            existing_user = UserRepository.find_by_username(user_data.username)
            if existing_user:
                raise ConflictException(ERROR_USERNAME_EXISTS)

            existing_email = UserRepository.find_by_email(user_data.email)
            if existing_email:
                raise ConflictException("Email already exists")

            password_hash: bytes = UserService._hash_password(user_data.password)

            user_id: int = UserRepository.create(
                username=user_data.username,
                email=user_data.email,
                password_hash=password_hash
            )

            token: str = UserService._generate_token(user_id, user_data.username)

            return {
                'message': SUCCESS_USER_REGISTERED,
                'user': {
                    'id': user_id,
                    'username': user_data.username,
                    'email': user_data.email
                },
                'token': token
            }, 201

        except (ValidationException, ConflictException, AuthenticationException):
            raise
        except ValidationError as e:
            raise ValidationException(f"Validation failed: {str(e)}")
        except Exception as e:
            raise ValidationException(f"Registration error: {str(e)}")

    @staticmethod
    def login(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            login_data: user_model.UserLogin = user_model.UserLogin(**data)

            user: Optional[Dict[str, Any]] = UserRepository.find_by_username(login_data.username)
            if not user:
                raise AuthenticationException(ERROR_INVALID_CREDENTIALS)

            if not UserService._verify_password(login_data.password, user['password']):
                raise AuthenticationException(ERROR_INVALID_CREDENTIALS)

            token: str = UserService._generate_token(user['id'], user['username'])

            return {
                'message': SUCCESS_LOGIN,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                },
                'token': token
            }, 200

        except (ValidationException, AuthenticationException, ConflictException):
            raise
        except ValidationError as e:
            raise ValidationException(f"Validation failed: {str(e)}")
        except Exception as e:
            raise AuthenticationException(ERROR_INVALID_CREDENTIALS)

    @staticmethod
    def verify_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
        if not token:
            return None

        try:
            payload: Dict[str, Any] = jwt.decode(token, UserService.SECRET_KEY, algorithms=[UserService.ALGORITHM])
            user_id: Optional[int] = payload.get('user_id')
            username: Optional[str] = payload.get('username')

            user: Optional[Dict[str, Any]] = UserRepository.find_by_id(user_id)
            if not user:
                return None

            return {
                'user_id': user_id,
                'username': username
            }

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None

    @staticmethod
    def logout(token: Optional[str]) -> Tuple[Dict[str, Any], int]:
        try:
            if not token:
                raise AuthenticationException(ERROR_UNAUTHORIZED)

            user: Optional[Dict[str, Any]] = UserService.verify_token(token)
            if not user:
                raise AuthenticationException(ERROR_UNAUTHORIZED)

            return {
                'message': 'Logout successful',
                'user_id': user['user_id']
            }, 200

        except AuthenticationException:
            raise
        except Exception as e:
            raise AuthenticationException(ERROR_UNAUTHORIZED)

