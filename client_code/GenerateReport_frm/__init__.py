from ._anvil_designer import GenerateReport_frmTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class GenerateReport_frm(GenerateReport_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def low_stock_btn_click(self, **event_args):
        '''reveal low stock report'''
        self.low_stock_crd.visible = True
        self.threshold_txb.focus()


    def best_seller_btn_click(self, **event_args):
        """
        calculates and displays a summary of which planys have 
        sold the most units in the last 30 days
        """
        pass

    def generate_btn_click(self, **event_args):
        """
        generates and displays a list of all plants where 
        the stock quantity is below a certain threshold
        """
        # GET and VALIDATE threshold qty
        if self.threshold_txb.text == '':
            alert('Threshold cannot be empty.')
            return
        
        try:
            threshold_val = int(self.threshold_txb.text)
        except:
            alert('Threshold must be a valid integer.')
            return
        
        if threshold_val < 0:
            alert('Threshold must be greater than or equal to zero.')
            return
