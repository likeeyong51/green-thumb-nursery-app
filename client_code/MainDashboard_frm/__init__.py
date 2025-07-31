from ._anvil_designer import MainDashboard_frmTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AddPlant_frm import AddPlant_frm
from ..RecordSale_frm import RecordSale_frm

class MainDashboard_frm(MainDashboard_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # GET user role
        self.role = properties['user_role']
        self.username = properties['username']
        if self.role == 'Manager':
            # show Add Plant option, which is accessible to managers and admin only
            self.add_plant_btn.visible = True

    def add_plant_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.load_pnl.clear()
        self.load_pnl.add_component(AddPlant_frm())

    def record_sale_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.load_pnl.clear()
        self.load_pnl.add_component(RecordSale_frm(username=self.username))
        
