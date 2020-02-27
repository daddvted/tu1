import subprocess
import asyncio
import urwid


def show_or_exit(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()

debug = urwid.Text('DEBUG')

async def update_text(read_data):
    pass
    # debug.set_text(f'retcode: {pipe.returncode}')
    # text.set_text(text.text + read_data.decode('utf-8'))


def enter_idle():
    loop.remove_watch_file(pipe.stdout)

async def get_date(stdout, stderr):

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        'python', '-u', 'job.py',
        stdout=stdout,
        stderr=stderr)

    # Read one line of output.
    # data = await proc.stdout.readline()
    # line = data.decode('utf-8').rstrip()

    # Wait for the subprocess exit.
    # await proc.wait()
    code = await proc.wait()
    print(code)
    # return line

if __name__ == '__main__':
    widget = urwid.Pile([
        debug,
        urwid.Button('And here another button'),
        urwid.Button('One more, just to be sure'),
        urwid.Button("Heck, let's add yet another one!"),
    ])
    text = urwid.Text('PROCESS OUTPUT:\n')
    widget = urwid.Columns([widget, text])
    widget = urwid.Filler(widget, 'top')

    loop = urwid.MainLoop(widget, unhandled_input=show_or_exit)
    stdout = loop.watch_pipe(update_text)
    stderr = loop.watch_pipe(update_text)
    get_date(stdout, stderr)
    loop.run()
