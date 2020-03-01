import queue
import logging
import threading
import subprocess

import urwid
from tui.componentchoice import ComponentChoice
from tui.uiwidgets import AppHeader, AppFooter, PopupDialog
from tui.introview import IntroView
from tui.progressview import ProgressView
from tui import conf

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-4s %(threadName)s %(message)s",
    datefmt="%H:%M:%S",
    filename='trace.log',
)


def order_jobs(jobs: list) -> list:
    logging.debug('input jobs: {}'.format(jobs))

    tmp = []
    for job in jobs:
        tmp.append((job, conf.ORDER[job]))
    tmp.sort(key=lambda x: x[1])

    ordered_jobs = [x[0] for x in tmp]
    logging.debug('output jobs: {}'.format(ordered_jobs))
    return ordered_jobs



class SetupWizard:
    # Set 'True' when opening quit popup,
    # disable other user input(see _unhandled_control())
    quitting = False

    def __init__(self):
        # Threading for invoke command/job
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.mq = queue.Queue()

        self.palette = conf.PALETTE
        self.last_content = None
        self.current_job = None
        self.jobs = []

        self.header = AppHeader()
        self.footer = AppFooter()

        self.current_content = IntroView()
        self.progress_view = None

        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop = urwid.MainLoop(view, self.palette, unhandled_input=self._unhandled_control)
        self._print_output(self.loop, None)

    def _run_command(self, cmd, stop_event, msg_queue, job):
        retry = 1
        # Run only one thread
        self.lock.acquire()
        self.header.debug2.set_text("current job: {}".format(job))

        self.progress_view.set_job_status(job, 'Installing', 'warning')

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
                if proc.returncode == 0:
                    self.progress_view.set_job_status(job, 'Success', 'success')
                    break
                else:
                    if retry < conf.RETRY_NUM:
                        self.progress_view.set_job_status(job, 'Retry (No.{})'.format(retry), 'warning')
                    else:
                        self.progress_view.set_job_status(job, 'FAILED', 'error')
                        import sys
                        sys.exit()
                retry += 1
        finally:
            # When job succeeded, release lock to run next thread
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
        self.progress_view.console.append(
            urwid.Text(('body', msg))
        )
        self.progress_view.output.set_focus(
            len(self.progress_view.console) - 1, 'above'
        )

    def _handle_install_event(self, *args):
        # self.header.debug.set_text('trigger install event')

        self.header.debug.set_text(','.join(self.current_content.components))
        self.jobs = order_jobs(self.current_content.components)

        self.progress_view = ProgressView(self.jobs)

        self.display_view(self.progress_view)

        for job in self.jobs:
            minion = threading.Thread(
                target=self._run_command,
                args=(conf.JOB_COMMAND[job], self.stop_event, self.mq, job),
                name=job
            )
            minion.start()
            # self.header.debug2.set_text("current job: {}".format(threading.current_thread()))

    def _handle_quit_event(self, widget, item):
        btn, = item
        if btn.label.lower() == 'yes':
            raise urwid.ExitMainLoop()
        else:
            self.quitting = False
            self.display_view(self.last_content)

    def _unhandled_control(self, key):
        self.header.debug.set_text('{}'.format(key))

        """Last resort for keypresses."""
        if not self.quitting:
            if key == "f2":
                self.header.debug.set_text("you press F2")
                component_choice = ComponentChoice()
                urwid.connect_signal(component_choice, 'install_event', self._handle_install_event)

                self.display_view(component_choice)

            elif key == "f4":
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


if __name__ == '__main__':
    # SetupWizard().main()
    wizard = SetupWizard()
    # wizard.main()
    wizard.loop.run()

    wizard.stop_event.set()
    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()
