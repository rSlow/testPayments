from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format


class MediaScrollFormat(Format):
    async def _render_text(
            self,
            data: dict,
            manager: DialogManager,
    ) -> str:
        full_data = data.copy()
        getter_data = data.get("data", {})
        full_data.update(**getter_data)

        return await super()._render_text(
            data=full_data,
            manager=manager
        )
