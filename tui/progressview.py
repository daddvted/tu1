import urwid
from tui.uiwidgets import JobBar


class ProgressView(urwid.WidgetWrap):
    def __init__(self, jobs):
        self._jobs = jobs

        self.flow_walker = urwid.SimpleListWalker([])
        self.output = urwid.ListBox(self.flow_walker)

        listbox_content = []
        for job in self._jobs:
            job_bar = JobBar(job, "running")
            listbox_content.append(job_bar)

        left = urwid.Pile(listbox_content)


        widget = self.output
        super().__init__(widget)
