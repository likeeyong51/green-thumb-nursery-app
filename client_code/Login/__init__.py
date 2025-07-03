from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class Login(LoginTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def login_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        # get and format the username
        email_for_login = f"{self.item['username']}@nursery.com"
        # attempt a log in
        try:
            anvil.users.login_with_email(email_for_login, self.item['password'])
            # if login is successful, open with main app form
            anvil.open_form('MainDashboard')
        except anvil.users.AuthenticationFailed as e:
            alert(str(e))

    def signup_lnk_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.open_form('Signup')
        
