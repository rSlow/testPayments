from abc import ABC
from typing import Optional

from aiohttp import ClientSession

from .models import UserModel


class BaseBackendAPI(ABC):
    def __init__(self,
                 local_base: Optional[str] = None,
                 global_base: Optional[str] = None):
        if not any((local_base, global_base)):
            raise ValueError("none of the values from the `local_base`, `global_base` have been set")

        self.__local_base = local_base
        self.__global_base = global_base

    @property
    def _base(self):
        if not self.__local_base:
            return self.__global_base
        return self.__local_base

    def _get_base(self, local: bool):
        return self._base if local else self.__global_base


class UserAPI(BaseBackendAPI):
    async def register_user(self,
                            session: ClientSession,
                            user_id: int):
        async with session.post(
                url=self._base + f"/users/{user_id}/",
                # data={"telegram_id": user_id}
        ) as response:
            user = await response.json()
        return UserModel.model_validate(user)

    async def get_user(self,
                       session: ClientSession,
                       user_id: int):
        async with session.get(self._base + f"/users/{user_id}/") as response:
            user = await response.json()
        return UserModel.model_validate(user)
