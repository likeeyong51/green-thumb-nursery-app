import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import bcrypt

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def get_role():
    '''return all roles from the role table'''
    return app_tables.role.search()

def get_hashed_password(email):
    '''get the hash_password for verification'''
    user = app_tables.users.get(email=email)

    if user:
        return user['password_hash'].encode('utf-8')

    return None

@anvil.server.callable
def signup_user(firstname, lastname, emp_id, role, password):
    '''Signs up a new user, ensuring the username is unique.'''
    username = firstname.replace(' ', '').lower() # remove spaces
    email = f"{username}@nursery.com"

    # check if a user with this first name already exists
    if app_tables.users.get(email=email) and verify_password(password, get_hashed_password(email)):
        # create a more unique username
        username = f"{firstname.replace(' ', '').lower()}{lastname.replace(' ', '').lower()}"
        email = f"{username}@nursery.com"

        # check again with the combined name
        if app_tables.users.get(email=email):
            raise anvil.server.ExecutionTerminatedError("A user with this name already exists.")

    # if username is unique, create the user account
    new_user = app_tables.users.add_row(
        email=email, 
        password_hash=password.decode('utf-8'), 
        role=role)

    return new_user

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Create a hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print(hashed_password)
    return hashed_password

def verify_password(password, hashed_password):
    # Check if the password matches the hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
