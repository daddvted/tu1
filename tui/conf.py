from collections import OrderedDict

HEADER_TEXT = "XXXXX Offline Setup Wizard"
FOOTER_TEXT = [
    " Continue", ('key', " F2 "),
    "    Quit", ('key', " F4 "),
]

PALETTE = [
    ('header', 'white', 'dark green', 'bold'),
    ('body', 'default', 'default'),
    ('footer', 'default', 'dark blue'),
    ('important', 'dark blue', 'light gray', ('standout', 'underline')),
    ('key', 'yellow', 'dark green'),
    ('background', 'default', 'light gray'),
    ('button', 'white', 'dark green', 'bold'),
    ('error', 'light red', 'black'),
    ('warning', 'yellow', 'default'),
    ('success', 'light green', 'default', 'standout'),
    ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
    ('debug', 'white', 'dark blue', 'bold'),
    ('success_bg', 'white', 'dark green', 'bold'),
    ('warning_bg', 'white', 'yellow', 'bold'),
    ('error_bg', 'white', 'dark red', 'bold'),
]

DEFAULT_WIDTH_PERCENTAGE = 80
DEFAULT_TOP_PADDING = 6

POPUP_BTN_WIDTH = 8
POPUP_WIDTH = 30
POPUP_HEIGHT = 6


ORDER = {
    'basic': 0,
    'xledger': 1,
    'luna': 2
}

COMPONENTS = {
    'basic': 'Basic Environment(Docker, Python)',
    'xledger': 'xLedger Platform',
    'luna': 'Luna Platform',
}

JOB_COMMAND = {
    'basic': ['python', '-u', 'job.py'],
    'luna': ['bash', 'job.sh'],
    'xledger': ['bash', 'job2.sh']
}
RETRY_NUM = 3

