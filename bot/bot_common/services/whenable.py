from typing import Self

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


class WhenAble:
    def __init__(self,
                 key: str,
                 flag: bool = True):
        self.key = key
        self.flag = flag

    def __call__(self,
                 data: dict,
                 _: Whenable,
                 __: DialogManager):
        result = data.get(self.key)
        return bool(result) == self.flag

    def __invert__(self) -> Self:
        return type(self)(self.key, not self.flag)
