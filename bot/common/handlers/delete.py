from aiogram import Router, types, F

delete_router = Router(name="delete")


@delete_router.message(F.text)
async def delete(message: types.Message):
    await message.delete()
