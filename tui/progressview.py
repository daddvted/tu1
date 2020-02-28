import urwid
from tui.uiwidgets import JobBar


class ProgressView(urwid.WidgetWrap):
    def __init__(self, jobs):
        self._jobs = jobs

        listbox_content = []
        for job in self._jobs:
            job_bar = JobBar(job, "running")
            listbox_content.append(job_bar)


        left = urwid.Pile(listbox_content)
        self.output = urwid.Text('hehe')
        # right = urwid.LineBox(self.output, title="Output")


        widget = urwid.Filler(urwid.Columns([left, self.output]), valign='top')
        super().__init__(widget)
