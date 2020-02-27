import urwid


class PackageChoice(urwid.WidgetWrap):
    signals = ['change_event']

    def __init__(self):
        self.options = []
        self.debug = urwid.Text('hehe')

        # To use 'user_data', set 'on_state_change'
        checkbox_list = [
            urwid.CheckBox("Basic Environment(Docker, Python)", on_state_change=self._emit_change, user_data='basic'),
            urwid.CheckBox("xLedger Platform", on_state_change=self._emit_change, user_data='xledger'),
            urwid.CheckBox("Luna Platform", on_state_change=self._emit_change, user_data="luna"),
        ]

        choice = urwid.Pile(checkbox_list)
        content = [
            urwid.Divider(top=6),
            urwid.Text(('title', 'Choose Component to Install:')),
            urwid.Divider(top=1),
            # urwid.AttrWrap(choice, 'header'),
            choice,
            urwid.Divider(),
            self.debug
        ]

        list_box = urwid.Padding(urwid.ListBox(urwid.SimpleListWalker(content)), width=('relative', 80), align="center")
        urwid.WidgetWrap.__init__(self, list_box)

    def _emit_change(self, *args):
        self._emit('change_event', args)

    def get_package_list(self):
        packages = []
        for cb in self.content:
            packages.append(cb.get_state())
            # if cb.get_state():
            #     packages.append(cb.label)

        return packages


class PopupDialog(urwid.WidgetPlaceholder):
    signals = ['quit_event']
    def __init__(self):
        super().__init__(urwid.SolidFill(' '))
        content = [
            urwid.Text("Quit Setup Wizard ?"),
            urwid.Columns([
                urwid.Button('Yes', on_press=self._emit_quit_event),
                urwid.Button('No', on_press=self._emit_quit_event),
            ])
        ]
        # urwid.WidgetWrap.__init__(self, urwid.ListBox(urwid.SimpleListWalker(content)))
        self.origin = urwid.ListBox(urwid.SimpleListWalker(content))
    def open(self):
        self.original_widget = urwid.Overlay(urwid.LineBox(self.origin),
                                             self.original_widget,
                                             align='center', width=('relative', 30),
                                             valign='middle', height=('relative', 30)
                                             )


    def _emit_quit_event(self, *args):
        self._emit('quit_event', args)




class StartView(urwid.WidgetWrap):
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
            urwid.Divider(top=6),
            urwid.Padding(text, align='center', width=('relative', 80)),
            urwid.Divider(),
        ]
        body_content = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

        body = urwid.AttrWrap(body_content, 'body')
        super().__init__(body)


class SetupWizard:
    palette = [
        ('header', 'white', 'dark green', 'bold'),
        ('body', 'default', 'default'),
        ('footer', 'default', 'dark blue'),
        ('title', 'light red', 'black'),
        ('important', 'dark blue', 'light gray', ('standout', 'underline')),
        ('key', 'yellow', 'dark green'),
        ('background', 'default', 'light gray'),
        ('editfc', 'white', 'dark green', 'bold'),
        ('editbx', 'light gray', 'dark blue'),
        ('editcp', 'black', 'light gray', 'standout'),
        ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
        ('debug', 'white', 'dark blue', 'bold'),
    ]

    header_text = ('header', [
        "XXXXX Offline Setup Wizard",
    ])

    footer_text = ('footer', [
        " Continue", ('key', " F2 "),
        "    Quit", ('key', " F4 "),
    ])

    components = []
    quitting = False

    def __init__(self):
        self.debug = urwid.AttrWrap(urwid.Text('DEBUG'), 'debug')

        self.last_content = None

        self.header = self._build_header()
        self.footer = self._build_footer()

        self.current_content = StartView()


        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop = urwid.MainLoop(view, self.palette, unhandled_input=self._unhandled_control)

    def _build_header(self):
        widget_list = [
            urwid.AttrWrap(urwid.Text(self.header_text), 'header'),
            self.debug,
        ]
        return urwid.Columns(widget_list)

    def _build_footer(self):
        return urwid.AttrWrap(urwid.Text(self.footer_text), 'footer')

    def _handle_change_event(self, *args):
        _, state, label = args[1]
        if state:
            if label not in self.components:
                self.components.append(label)
        else:
            try:
                self.components.remove(label)
            except ValueError:
                pass

        self.debug.set_text(','.join(self.components))
        # self.debug.set_text(f'{user_data}')

    def _handle_quit_event(self, widget, item):
        btn, = item
        self.debug.set_text(f'{btn.label.lower()}')
        if btn.label.lower() == 'yes':
            self._quit()
        else:
            self.quitting = False
            self.set_view(self.last_content)


    def _quit(self):
        raise urwid.ExitMainLoop()

    def _unhandled_control(self, k):
        """Last resort for keypresses."""
        if not self.quitting:
            if k == "f2":
                self.debug.set_text("you press F2")
                package_choice = PackageChoice()
                urwid.connect_signal(package_choice, 'change_event', self._handle_change_event)
                self.set_view(package_choice)

            elif k == "f4":
                self.debug.set_text("you press F4")
                self.quitting = True
                popup = PopupDialog()
                urwid.connect_signal(popup, 'quit_event', self._handle_quit_event)
                popup.original_widget = self.current_content
                popup.open()
                self.set_view(popup)

            else:
                return
        return True

    def set_view(self, widget):
        self.last_content = self.current_content
        self.current_content = widget
        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop.widget = view


    def main(self):
        self.loop.run()


if __name__ == '__main__':
    SetupWizard().main()
