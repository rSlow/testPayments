from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from config import settings

redis_storage = RedisStorage.from_url(
    url=settings.REDIS_URL,
    key_builder=DefaultKeyBuilder(with_destiny=True)
)
