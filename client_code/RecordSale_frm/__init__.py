from ._anvil_designer import RecordSale_frmTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RecordSale_frm(RecordSale_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.item = {}
        # get plant list from current plant inventory
        plant_list = anvil.server.call('get_plant_list')
        self.plant_drp.items = [plant['name'] for plant in plant_list]
        
        # delay focus until form loads properly
        anvil.js.window.setTimeout(lambda: self.plant_drp.focus(), 100)

    def record_sale_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
