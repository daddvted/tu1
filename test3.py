import subprocess
import logging, sys, threading, time
try:
    import queue as Queue
except ImportError:
    import Queue

import urwid

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-4s %(threadName)s %(message)s",
    datefmt="%H:%M:%S",
    filename='trace.log',
)


class Worker(threading.Thread):
    def __init__(self, cmd):
        super().__init__()
        self._cmd = cmd

    def run(self) -> None:
        proc = subprocess.Popen(
            ['python', '-u', 'job.py'],
        )
        while proc.poll() is None:
            break



class Interface:
    palette = [
        ('body', 'white', 'black'),
        ('ext', 'white', 'dark blue'),
        ('ext_hi', 'light cyan', 'dark blue', 'bold'),
        ]

    header_text = [
        ('ext_hi', 'ESC'), ':quit        ',
        ('ext_hi', 'UP'), ',', ('ext_hi', 'DOWN'), ':scroll',
        ]

    def __init__(self, msg_queue):
        self.header = urwid.AttrWrap(urwid.Text(self.header_text), 'ext')
        self.flowWalker = urwid.SimpleListWalker([])
        self.body = urwid.ListBox(self.flowWalker)
        # self.footer = urwid.AttrWrap(urwid.Edit("Edit:  "), 'ext')
        self.footer = urwid.Text('DEBUG')
        self.view = urwid.Frame(
            urwid.AttrWrap(self.body, 'body'),
            header = self.header,
            footer = self.footer)
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input = self.unhandled_input)
        self.msg_queue = msg_queue
        self.check_messages(self.loop, None)

    def unhandled_input(self, k):
        if k == 'esc':
            raise urwid.ExitMainLoop()

    def check_messages(self, loop, *_args):
        """add message to bottom of screen"""
        loop.set_alarm_in(
            sec=0.1,
            callback=self.check_messages,
        )
        # self.footer.set_text(self.msg_queue.get_nowait())
        try:
            msg = self.msg_queue.get_nowait()
        except Queue.Empty:
            self.footer.set_text('queuu empty')
            return
        self.footer.set_text('msg')
        self.flowWalker.append(
            urwid.Text(('body', msg))
            )
        self.body.set_focus(
            len(self.flowWalker)-1, 'above'
            )

def update_time(stop_event, msg_queue):
    """send timestamp to queue every second"""
    logging.info('start')
    while not stop_event.wait(timeout=0.1):
        proc = subprocess.Popen(
            ['python', '-u', 'job.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        while proc.poll() is None:
            line = proc.stdout.readline().rstrip()
            msg_queue.put(line)
        msg_queue.put("Thread done: {}".format(proc.returncode))
        break

        # msg_queue.put( time.strftime('time %X') )
    logging.info('stop')

if __name__ == '__main__':

    stop_ev = threading.Event()
    message_q = Queue.Queue()

    logging.info(stop_ev.is_set())

    threading.Thread(
        target=update_time, args=(stop_ev, message_q),
        name='update_time',
    ).start()

    logging.info('start')
    Interface(message_q).loop.run()
    logging.info('stop')

    # after interface exits, signal threads to exit, wait for them
    logging.info('stopping threads')

    stop_ev.set()
    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()