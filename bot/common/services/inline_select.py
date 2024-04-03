from abc import abstractmethod
from typing import Sequence, Any, Protocol, Callable, Optional

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InlineFactory(Protocol):
    @abstractmethod
    def __call__(self, item: Any) -> InlineKeyboardButton:
        ...


class InlineSelect(InlineKeyboardBuilder):
    previous_page = "prev_page"
    next_page = "next_page"

    def __init__(self,
                 page_key: str,
                 items: Sequence[Any],
                 fsm_context: FSMContext,
                 main_func: Callable,
                 main_func_kwargs: Optional[dict[str, Any]] = None,
                 factory: Optional[InlineFactory] = None,
                 on_page: int = 6,
                 markup: list[list[InlineKeyboardButton]] | None = None):
        super().__init__(markup)

        self.page_key = page_key
        self.items = items
        self.factory = factory
        self.fsm_context = fsm_context
        self.main_func = main_func
        self.main_func_kwargs = main_func_kwargs or {}
        self.on_page = on_page

        self.__current_page = 1

    @property
    def items_count(self):
        return len(self.items)

    @property
    def pages(self):
        items_count = self.items_count
        return items_count // self.on_page + int((items_count % self.on_page) != 0)

    def register_pagination(self,
                            router: Router,
                            fsm_state: State):
        async def _current_page_callback(callback: types.CallbackQuery):
            await callback.answer()

        async def _pagination_callback(callback: types.CallbackQuery,
                                       state: FSMContext):
            data = await state.get_data()
            current_page = data.get(self.page_key)
            new_page = current_page

            match callback.data:
                case self.previous_page:
                    if current_page > 1:
                        new_page -= 1
                case self.next_page:
                    if current_page < self.pages:
                        new_page += 1
                case _:
                    raise RuntimeError(f"unknown callback data `{callback.data}`")
            if new_page != current_page:
                await self.fsm_context.update_data({self.page_key: new_page})
                await self.main_func(
                    callback=callback,
                    state=state,
                    **self.main_func_kwargs
                )
            else:
                await callback.answer()

        router.callback_query.register(
            _pagination_callback,
            F.data.in_([self.previous_page, self.next_page]),
            fsm_state
        )
        router.callback_query.register(
            _current_page_callback,
            F.data == "current_page",
            fsm_state
        )

    async def paginate(self):
        data = await self.fsm_context.get_data()
        __current_page = data.get(self.page_key)
        if __current_page is None:
            __current_page = 1
        self.__current_page = __current_page
        await self.fsm_context.update_data({self.page_key: self.__current_page})

        if self.factory is not None:
            start = (self.__current_page - 1) * self.on_page
            stop = self.__current_page * self.on_page
            items_to_show = self.items[start:stop]
            buttons = [self.factory(item) for item in items_to_show]
            self.add(*buttons)
            self.adjust(*[1 for _ in range(self.on_page)])

        if self.items_count > self.on_page:
            self.row(
                InlineKeyboardButton(
                    text="<",
                    callback_data=self.previous_page
                ),
                InlineKeyboardButton(
                    text=f"{self.__current_page}",
                    callback_data="current_page"
                ),
                InlineKeyboardButton(
                    text=">",
                    callback_data=self.next_page
                ),
            )
