from aiogram_dialog.widgets.common import Scroll, WhenCondition
from aiogram_dialog.widgets.kbd import Row, FirstPage, PrevPage, CurrentPage, NextPage, LastPage
from aiogram_dialog.widgets.text import Format


class PagerScroll(Row):
    def __init__(self,
                 scroll: str | Scroll | None,
                 when: WhenCondition = None):
        super().__init__(
            FirstPage(
                scroll=scroll,
                text=Format("{target_page1}"),
            ),
            PrevPage(
                scroll=scroll,
                text=Format("◀"),
            ),
            CurrentPage(
                scroll=scroll,
                text=Format("{current_page1}"),
            ),
            NextPage(
                scroll=scroll,
                text=Format("▶"),
            ),
            LastPage(
                scroll=scroll,
                text=Format("{target_page1}"),
            ),
            when=when
        )
