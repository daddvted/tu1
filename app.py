import urwid
from tui.componentchoice import ComponentChoice
from tui.uiwidgets import AppHeader, AppFooter, PopupDialog
from tui.introview import IntroView
from tui.conf import palette


class SetupWizard:

    # Set 'True' when opening quit popup,
    # disable other user input(see _unhandled_control())
    quitting = False

    def __init__(self):
        self.palette = palette

        self.last_content = None

        self.header = AppHeader()
        self.footer = AppFooter()

        self.current_content = IntroView()

        view = urwid.Frame(self.current_content, header=self.header, footer=self.footer)
        self.loop = urwid.MainLoop(view, self.palette, unhandled_input=self._unhandled_control)



    def _handle_install_event(self, *args):
        # self.header.debug.set_text('trigger install event')

        self.header.debug.set_text(','.join(self.current_content.components))

    def _handle_quit_event(self, widget, item):
        btn, = item
        self.header.debug.set_text(f'{btn.label.lower()}')
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
                self.header.debug.set_text("you press F2")
                package_choice = ComponentChoice()
                urwid.connect_signal(package_choice, 'install_event', self._handle_install_event)

                self.set_view(package_choice)

            elif k == "f4":
                self.header.debug.set_text("you press F4")
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
