import urwid
from tui import conf


class ComponentChoice(urwid.WidgetWrap):
    signals = ['install_event']

    def __init__(self):
        self.options = []
        self.warning = urwid.Text('')
        self._components = []

        # To use 'user_data', set 'on_state_change'
        checkboxes = [
            urwid.CheckBox("Basic Environment(Docker, Python)", on_state_change=self._handle_checkbox_change, user_data='basic'),
            urwid.CheckBox("xLedger Platform", on_state_change=self._handle_checkbox_change, user_data='xledger'),
            urwid.CheckBox("Luna Platform", on_state_change=self._handle_checkbox_change, user_data="luna"),
        ]
        choice = urwid.Pile(checkboxes)

        install_btn = urwid.Padding(urwid.Button(('button','Install'), on_press=self._handle_button_click),
                      width=('relative', 10), align='left', min_width=10)
        # install_btn = urwid.AttrWrap(install_btn, 'button')

        content = [
            urwid.Divider(top=conf.DEFAULT_TOP_PADDING),
            urwid.Text(('error', 'Choose Component to Install:')),
            urwid.Divider(),
            choice,
            urwid.Divider(),
            urwid.AttrWrap(self.warning, 'warning'),
            urwid.Divider(),
            install_btn
        ]

        widget = urwid.Padding(urwid.ListBox(urwid.SimpleListWalker(content)), width=('relative', 50), align="center")
        # widget = urwid.AttrWrap(widget, 'body')
        urwid.WidgetWrap.__init__(self, widget)

    def _handle_checkbox_change(self, *args):
        _, state, label = args
        if state:
            if label not in self._components:
                self._components.append(label)
        else:
            try:
                self._components.remove(label)
            except ValueError:
                pass

    def _handle_button_click(self, *args):
        if self._components:
            self._emit('install_event', args)
        else:
            self.warning.set_text('Choose component to install')


    @property
    def components(self):
        return self._components
