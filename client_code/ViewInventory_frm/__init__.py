from ._anvil_designer import ViewInventory_frmTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ViewInventory_frm(ViewInventory_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        

    def view_inventory_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        # get plant list from current plant inventory
        plant_list = anvil.server.call('get_plant_list')
        # add it to the dropdown item list
        # self.drop_down_1.items = [plant['name'] for plant in plant_list]
        # dropdown_items = [plant['name'] for plant in plant_list]
        # print([plant for plant in plant_list])
        if plant_list:
            self.inventory_list_rpnl.items = [plant for plant in plant_list]
            self.inventory_crd.visible = True
