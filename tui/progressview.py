import urwid
from tui.uiwidgets import JobBar


class ProgressView(urwid.WidgetWrap):
    def __init__(self, jobs):
        self._jobs = jobs

        listbox_content = []
        for job in self._jobs:
            job_bar = JobBar(job, "running")
            listbox_content.append(job_bar)

        widget = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        super().__init__(widget)
