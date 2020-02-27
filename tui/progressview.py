import urwid
from tui.uiwidgets import JobBar


class ProgressView(urwid.WidgetWrap):
    def __init__(self):
        listbox_content = [
            JobBar("Job-a", "running"),
        ]

        widget = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        super().__init__(widget)
