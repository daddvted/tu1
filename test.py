import subprocess
import asyncio
import urwid
import time
import os
import sys

debug = urwid.Text('debug')

def exit_on_enter(key):
    if key == 'enter': raise urwid.ExitMainLoop()

def received_output(data):
    output_widget.set_text(output_widget.text + data.decode('utf8'))

def on_click(*args):
    debug.set_text(f'{args}')

    with subprocess.Popen(
        # ['bash', 'job.sh'],
        ['python', '-u', 'job.py'],
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        ) as p:
        for line in p.stdout:
            output_widget.set_text(output_widget.text + line)
        debug.set_text(f'retcode: {p.returncode}')

    # proc.wait()
    # debug.set_text(f'{proc.pid}: {proc.returncode}')


output_widget = urwid.Text("hehe")
footer = urwid.Button("work", on_press=on_click)
frame_widget = urwid.Frame(
    header=debug,
    body=urwid.Filler(output_widget, valign='middle'),
    footer=footer
)



loop = urwid.MainLoop(frame_widget, unhandled_input=exit_on_enter)
# write_fd = loop.watch_pipe(received_output)

# while proc.poll() is None:
#     line = proc.stdout.read()
#     debug.set_text(line)
# debug.set_text(f'{proc.pid}: {proc.returncode}')

# debug.set_text(proc.wait())

# check(proc)
loop.run()


