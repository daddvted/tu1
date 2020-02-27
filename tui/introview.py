import urwid

from tui import conf

class IntroView(urwid.WidgetWrap):
    text_intro = [
        ('important', 'Valar Morghulis'),
        ' is a Braavosi greeting said in the High Valyrian language,',
        ' which literally translates to ',
        ('important', "All men must die"),
        ' in the Common Tongue. ',
        ('important', 'Valar Dohaeris'),
        ' is its accompanying greeting, which literally translates to ',
        ('important', "All men must serve"),
        "."
    ]

    def __init__(self):
        text = urwid.Text(self.text_intro)

        listbox_content = [
            urwid.Divider(top=conf.DEFAULT_TOP_PADDING),
            urwid.Padding(text, align='center', width=('relative', conf.DEFAULT_WIDTH_PERCENTAGE)),
            urwid.Divider(),
        ]
        body_content = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        widget = urwid.AttrWrap(body_content, 'body')
        super().__init__(widget)
