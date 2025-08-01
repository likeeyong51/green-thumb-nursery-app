from ._anvil_designer import Splash_frmTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Splash_frm(Splash_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.timer_1.interval = 1 # 1 sec interval per tick
        self.time             = 3 # 3 secs countdown

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.time == 0:
            open_form('Login_frm')
        else:
            self.time -= 1
