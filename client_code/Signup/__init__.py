from ._anvil_designer import SignupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import Notification

class Signup(SignupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.item['firstname'] = \
        self.item['lastname']  = \
        self.item['emp_id']    = \
        self.item['role']      = \
        self.item['password']  = None
        # populate dropdown list items from role table
        self.role_drp.items = [r['role'] for r in anvil.server.call('get_role')]

    def signup_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        # check if any of the required fields (firstname, role and password) is empty
        if not all([
            self.item['firstname'], 
            self.item['lastname'], 
            self.item['emp_id'], 
            self.item['role'], 
            self.item['password']
        ]):
            alert("All fields are required.")
            return

        try:
            if anvil.server.call(
                'signup_user', 
                self.item['firstname'], 
                self.item['lastname'], 
                self.item['emp_id'], 
                self.item['role'], 
                self.item['password']):
                # if signup is successful, notify user with success message
                Notification('Account created successfully!  Please log in.').show()
                # go back to the login form
                anvil.open_form('Login')
        except Exception as e:
            alert(str(e))