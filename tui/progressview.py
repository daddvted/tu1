import urwid
from tui.uiwidgets import JobBar


class ProgressView(urwid.WidgetWrap):
    def __init__(self, jobs):
        self._jobs = jobs

        self.console = urwid.SimpleListWalker([])
        self.output = urwid.ListBox(self.console)

        listbox_content = []
        for job in self._jobs:
            job_bar = JobBar(job, "running")
            listbox_content.append(job_bar)

        left_widget = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        right_widget = urwid.LineBox(self.output)

        # widget = self.output
        widget = urwid.Columns([left_widget, right_widget])
        super().__init__(widget)
