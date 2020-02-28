import threading
import queue
import subprocess

import urwid
from tui.componentchoice import ComponentChoice
from tui.uiwidgets import AppHeader, AppFooter, PopupDialog
from tui.introview import IntroView
from tui.progressview import ProgressView
from tui.conf import palette


class SetupWizard:
    # Set 'True' when opening quit popup,
    # disable other user input(see _unhandled_control())
    quitting = False

    def __init__(self):
        # Threading for invoke command/job
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.mq = queue.Queue()

        self.palette = palette

        self.last_content = None
        self.current_job = None

        self.header = AppHeader()
        self.footer = AppFooter()

        self.current_content = IntroView()

        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop = urwid.MainLoop(view, self.palette, unhandled_input=self._unhandled_control)
        self._print_output(self.loop, None)

    def _run_command(self, cmd, stop_event, msg_queue):
        self.lock.acquire()
        # with self.lock:
        try:
            while not stop_event.wait(timeout=0.1):
                proc = subprocess.Popen(
                    # ['python', '-u', 'job.py'],
                    # ['bash', 'job.sh'],
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                while proc.poll() is None:
                    line = proc.stdout.readline().rstrip()
                    msg_queue.put(line)
                msg_queue.put("Job Done, retcode: {}".format(proc.returncode))
                break
        finally:
            self.lock.release()

    def _print_output(self, loop, *_args):
        """add message to bottom of screen"""
        loop.set_alarm_in(
            sec=0.1,
            callback=self._print_output,
        )
        # self.footer.set_text(self.msg_queue.get_nowait())
        self.header.debug.set_text('{}'.format(threading.active_count()))
        try:
            msg = self.mq.get_nowait()
        except queue.Empty:
            # Debug
            self.header.debug.set_text('queue empty')
            return

        # Current content should be ProgressView()
        self.current_content.flow_walker.append(
            urwid.Text(('body', msg))
            )
        self.current_content.output.set_focus(
            len(self.current_content.flow_walker)-1, 'above'
            )

    def _handle_install_event(self, *args):
        # self.header.debug.set_text('trigger install event')

        self.header.debug.set_text(','.join(self.current_content.components))
        progress = ProgressView(self.current_content.components)
        for cmd in [
            ['python', '-u', 'job.py'],
            ['bash', 'job.sh'],
        ]:
            minion = threading.Thread(
                target=self._run_command,
                args=(cmd, self.stop_event, self.mq),
                name='Minion'
            )
            minion.start()
            self.header.debug2.set_text("{}".format(self.stop_event.is_set()))

        self.display_view(progress)

    def _handle_quit_event(self, widget, item):
        btn, = item
        if btn.label.lower() == 'yes':
            raise urwid.ExitMainLoop()
        else:
            self.quitting = False
            self.display_view(self.last_content)

    def _unhandled_control(self, k):
        """Last resort for keypresses."""
        if not self.quitting:
            if k == "f2":
                self.header.debug.set_text("you press F2")
                package_choice = ComponentChoice()
                urwid.connect_signal(package_choice, 'install_event', self._handle_install_event)

                self.display_view(package_choice)

            elif k == "f4":
                self.header.debug.set_text("you press F4")
                self.quitting = True
                popup = PopupDialog()
                urwid.connect_signal(popup, 'quit_event', self._handle_quit_event)
                popup.original_widget = self.current_content
                popup.open()
                self.display_view(popup)

            else:
                return
        return True

    def display_view(self, widget):
        self.last_content = self.current_content
        self.current_content = widget
        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop.widget = view

    # def main(self):
    #     self.loop.run()


if __name__ == '__main__':
    # SetupWizard().main()
    wizard = SetupWizard()
    # wizard.main()
    wizard.loop.run()

    wizard.stop_event.set()
    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()
