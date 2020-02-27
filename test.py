import urwid


palette = [
    ('body', 'default', 'default'),
    ('foot', 'dark cyan', 'dark blue', 'bold'),
    ('key', 'light cyan', 'dark blue', 'underline'),
]

# txt = urwid.Text(('foot', "Hello World"))
txt = urwid.Text(('foot', [u"nesting example ", ('key', u"inside"), u" outside"]))
fill = urwid.Filler(txt, 'middle')
loop = urwid.MainLoop(fill, palette=palette)
loop.run()
