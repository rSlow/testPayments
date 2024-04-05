from abc import ABC
from typing import Optional

from aiohttp import ClientSession

from .models import UserModel


class BaseBackendAPI(ABC):
    def __init__(self,
                 local_url: Optional[str] = None,
                 global_url: Optional[str] = None):
        if not all((local_url, global_url)):
            raise ValueError("none of the values from the `local_url`, `global_url` have been set")

        self.__local_url = local_url
        self.__global_url = global_url

    @property
    def _base(self):
        if not self.__local_url:
            return self.__global_url
        return self.__local_url

    def _get_base(self, local: bool):
        return self._base if local else self.__global_url


class UserAPI(BaseBackendAPI):
    async def get_user(self,
                       session: ClientSession,
                       user_id: int):
        async with session.get(self._base + f"/users/{user_id}") as response:
            user = await response.json()
        return UserModel.model_validate(user)
