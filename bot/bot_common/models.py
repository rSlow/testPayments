from pydantic import BaseModel


class UserModel(BaseModel):
    pk: int
    telegram_id: int
    is_active: bool
