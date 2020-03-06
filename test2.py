import urwid


lists = [
    urwid.Text('apple'),
    urwid.Text('banana'),
    urwid.Text('pear')
]

lists = [
    urwid.CheckBox('apple'),
    urwid.CheckBox('banana'),
    urwid.CheckBox('pear')
]

# left = urwid.ListBox(urwid.SimpleListWalker(lists))
left = urwid.Pile(lists)


right = urwid.Text(u"Hello World")
right = urwid.LineBox(right)


widgets = urwid.Columns([left, right])

content = urwid.Filler(widgets, valign='middle')

frame = urwid.Frame(body=content)
loop = urwid.MainLoop(frame)
loop.run()
