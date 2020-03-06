from collections import OrderedDict
import urwid
from tui.uiwidgets import JobBar
from tui import conf


class ProgressView(urwid.WidgetWrap):
    def __init__(self, jobs):
        self._jobs = jobs

        self.console = urwid.SimpleListWalker([])
        self.console_box = urwid.ListBox(self.console)

        self.job_bars = OrderedDict()
        for key in self._jobs:
            self.job_bars[key] = JobBar(conf.COMPONENTS[key], "Waiting")

        left_widget = urwid.Filler(urwid.Pile(self.job_bars.values()), valign='middle')

        right_widget = urwid.LineBox(self.console_box)

        # widget = self.output
        # widget = urwid.Columns([left_widget, right_widget])
        widget = urwid.Columns([left_widget, right_widget])
        super().__init__(widget)

    def set_job_status(self, job: str, status: str, color: str):
        text = (color, status)
        self.job_bars[job].status = text


