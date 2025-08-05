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
        """Loads and shows the plant inventory"""
        # hide the sales log card
        self.sales_log_crd.visible = False
        
        # get plant list from current plant inventory
        plant_list = anvil.server.call('get_plant_list')
        # add it to the dropdown item list
        # self.drop_down_1.items = [plant['name'] for plant in plant_list]
        # dropdown_items = [plant['name'] for plant in plant_list]
        # print([plant for plant in plant_list])
        if plant_list:
            self.inventory_list_rpnl.items = [plant for plant in plant_list]
            self.inventory_crd.visible = True

    def sales_log_btn_click(self, **event_args):
        """loads and shows the sales log"""
        # hide the inventory list card
        self.inventory_crd.visible = False

        # get sales list from current sales log
        sales_list = anvil.server.call('get_sales_list')

        self.build_sales_list(sales_list)
        # if sales_list exists
        # if sales_list:
        #     self.sales_list_rpnl.items = [sale for sale in sales_list]
        #     self.sales_log_crd.visible = True
        # else:
        #     alert('Sales list not found.')

    def date_filter_dpk_change(self, **event_args):
        """This method is called when the selected date changes"""
        # get the date to filter
        date = self.date_filter_dpk.date
        # print(date)
        sales_list = anvil.server.call('get_sales_list', date)

        self.build_sales_list(sales_list)
        
    def build_sales_list(self, sales_list, show=True):
        '''build the sales list'''
        if sales_list:
            self.sales_list_rpnl.items = [sale for sale in sales_list]
            self.sales_log_crd.visible = show
        else:
            self.sales_list_rpnl.items = None
            alert('Sales list not found.')