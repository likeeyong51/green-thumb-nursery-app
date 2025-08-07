import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
def add_plant(plant_info):
    '''add a new plant and return the add status'''
    # if new plant
    if not app_tables.plant_inventory.get(name=plant_info['name']):
        # then add plant
        return app_tables.plant_inventory.add_row(**plant_info)

    # plant already exists
    return False

@anvil.server.callable
def get_plant_list():
    ''' retrieve and returns a list of plants from the inventory list'''
    plant_list = app_tables.plant_inventory.search()
    if plant_list:
        return plant_list

    return False # error

@anvil.server.callable
def get_sales_list(date=None):
    '''retrieve and returns a list of sales from the sales log'''
    # fetch row based on date filter
    sales_row = (
        app_tables.sales_log.search(sale_date=date) if date
        else app_tables.sales_log.search() # or get everything
    )
    sales_data = []
    
    # build the inventory list
    for sale in sales_row or []:
        # build and append a single sale record for each sale_row
        plant = sale['plant_sold']  if sale['plant_sold'] else None
        user  = sale['recorded_by'] if sale['recorded_by'] else None
        
        sales_data.append({
            'plant_sold'   : plant['name'] if plant else 'Unknown',
            'quantity_sold': sale['quantity_sold'],
            'sale_date'    : sale['sale_date'],
            'recorded_by'  : user['email'].split('@')[0] if user else 'Unknown'
        })
    # print(sales_data)
    return sales_data if sales_data else False


@anvil.server.callable
def record_sale(sale):
    '''records a transaction sale'''
    # CHECK if qty sold <= available stock
    plant = app_tables.plant_inventory.get(name=sale['plant_sold'])
    
    if sale['quantity_sold'] > plant['stock_qty']:
        # qty not available
        return False, plant['stock_qty']
        
    # CREATE a row in the Sales_Log table
    # retrieve user record
    print(sale['recorded_by'])
    sale['recorded_by'] = app_tables.users.get(email=f"{sale['recorded_by'].lower()}@nursery.com")
    # set plant sold
    sale['plant_sold'] = plant
    # SAVE to the sales_log table
    if app_tables.sales_log.add_row(**sale):
        # if SAVE successful, UPDATE the stock quantity in the Plant_inventory table
        plant['stock_qty'] -= sale['quantity_sold']
        return True, plant['stock_qty']  # sales transaction completed successfully

    return False, -1 # sales transaction failed

