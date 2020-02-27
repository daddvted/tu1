import urwid

class QuestionnaireItem(urwid.WidgetWrap):
    def __init__(self):
        self.options = []
        unsure = urwid.RadioButton(self.options, u"Unsure")
        yes = urwid.RadioButton(self.options, u"Yes")
        no = urwid.RadioButton(self.options, u"No")
        display_widget = urwid.GridFlow([unsure, yes, no], 15, 3, 1, 'left')
        urwid.WidgetWrap.__init__(self, display_widget)

    def get_state(self):
        for o in self.options:
            if o.get_state() is True:
                return o.get_label()


fill = urwid.Filler(urwid.Padding(QuestionnaireItem(), 'center', 15))

txt = urwid.Text('hello world')
btn = urwid.Button('OK')


def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    txt.set_text(repr(key))


if __name__ == '__main__':
    loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
    loop.run()
