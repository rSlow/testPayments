from functools import wraps
from typing import Coroutine, Callable, Any

from aiogram.fsm.context import FSMContext


def add_context(*keys: tuple[str, Any]):
    _items = {key[0]: key[1] for key in keys}

    def decorator(func: Callable[..., Coroutine]):
        @wraps(func)
        async def inner(*args, **kwargs):
            state = kwargs.get("state")
            if isinstance(state, FSMContext):
                data = await state.get_data()

                for _key, _value in _items.items():
                    if _key not in data:
                        data[_key] = _value
                    else:
                        _items[_key] = data[_key]

                await state.update_data(data)

            result = await func(*args, **kwargs, **_items)
            return result

        return inner

    return decorator
