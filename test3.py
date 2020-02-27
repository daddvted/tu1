import asyncio
import sys

async def get_date():

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        'python', '-u', 'job.py',
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('utf-8').rstrip()

    # Wait for the subprocess exit.
    # await proc.wait()
    code = await proc.wait()
    print(code)
    return line

date = asyncio.run(get_date())
print(f"Current date: {date}")