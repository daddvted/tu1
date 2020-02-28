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

async def get_date(*args):
    # code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        'python', '-u', 'job.py',
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()
    output_widget.set_text(line)


    # Wait for the subprocess exit.

# async def on_click(*args):
#     debug.set_text('{}'.format(args))
#
#     # write_d = loop.watch_pipe(received_output)
#
#     proc = subprocess.Popen(
#         ['python', '-u', 'job.py', ';', 'echo'])
#
#     while proc.poll() is None:
#         output_widget.set_text('job still running')



    # debug.set_text('{}'.format(proc.returncode))

output_widget = urwid.Text("hehe")
footer = urwid.Button("work", on_press=get_date)
frame_widget = urwid.Frame(
    header=debug,
    body=urwid.Filler(output_widget, valign='middle'),
    footer=footer
)

evl = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())

loop = urwid.MainLoop(frame_widget, unhandled_input=exit_on_enter, event_loop=evl)
    # proc.wait()
    # debug.set_text(f'{proc.pid}: {proc.returncode}')


# write_fd = loop.watch_pipe(received_output)

# while proc.poll() is None:
#     line = proc.stdout.read()
#     debug.set_text(line)
# debug.set_text(f'{proc.pid}: {proc.returncode}')

# debug.set_text(proc.wait())

# check(proc)
loop.run()


