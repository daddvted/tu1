import subprocess
import asyncio
import urwid
import time
import os
import sys


debug = urwid.Text('debug')
output_widget = urwid.Text("hehe")
frame_widget = urwid.Frame(
    header=debug,
    body=urwid.Filler(output_widget, valign='middle'), )

def exit_on_enter(key):
    if key == 'enter': raise urwid.ExitMainLoop()

def check(proc: subprocess.Popen):
    while proc.poll() is not None:
        debug.set_text(f'{proc.poll()}')
        time.sleep(3)
        raise urwid.ExitMainLoop()



def received_output(data):
    output_widget.set_text(output_widget.text + data.decode('utf8'))


loop = urwid.MainLoop(frame_widget, unhandled_input=exit_on_enter)
write_fd = loop.watch_pipe(received_output)

proc = subprocess.Popen(
    ['python', '-u', 'job.py'],
    stdout=write_fd,
    stderr=write_fd,
    close_fds=True)

debug.set_text(f'{type(write_fd)}')





# debug.set_text(proc.wait())

# check(proc)

loop.run()


