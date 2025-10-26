from fastapi.openapi.models import Schema


class UserSchema(Schema):
    id: int
    name: str
    email: str
    password: str


class CreateUser(UserSchema):
    name: str
    email: str
    password: str


class UserResponse(UserSchema):
    id: int
    name: str
    email: str
