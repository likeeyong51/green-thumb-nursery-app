import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
import json
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from anvil import BlobMedia

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
    
    return plant_list if plant_list else False

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
def get_low_stock_list(threshold):
    # GET low-stock list based on threshold
    low_stock_list = app_tables.plant_inventory.search(
        stock_qty=q.less_than_or_equal_to(threshold)
    )

    return low_stock_list if low_stock_list else False

@anvil.server.callable
def download_low_stock_json(threshold):
    rows = get_low_stock_list(threshold)
    if not rows:
        return False

    data = [
        {
            'name'     : row['name'],
            'type'     : row['type'] if row['type'] else 'Uncategorised',
            'price'    : row['price'],
            'stock_qty': row['stock_qty']
        }
        for row in rows
    ]

    json_str = json.dumps(data, indent=2)
    return BlobMedia("application/json", json_str.encode('utf-8'), name="low_stock_report.json")

@anvil.server.callable
def download_low_stock_csv(threshold):
    rows = get_low_stock_list(threshold)
    if not rows:
        return False

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "type", "price", "stock_qty"])
    writer.writeheader()
    for row in rows:
        writer.writerow({
            'name'     : row['name'],
            'type'     : row['type'] if row['type'] else 'Uncategorised',
            'price'    : row['price'],
            'stock_qty': row['stock_qty']
        })

    return BlobMedia("text/csv", output.getvalue().encode('utf-8'), name="low_stock_report.csv")

@anvil.server.callable
def download_low_stock_pdf(threshold):
    rows = get_low_stock_list(threshold)
    if not rows:
        return False

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 12)
    y = height - 50
    c.drawString(50, y, f"Low Stock Report (Threshold ≤ {threshold})")
    y -= 30

    for row in rows:
        line = f"{row['name']} — Qty: {row['stock_qty']}, Type: {row['type'] if row['type'] else 'Uncategorised'}, Unit Price: ${row['price']:.2f}"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return BlobMedia("application/pdf", buffer.getvalue(), name="low_stock_report.pdf")

@anvil.server.callable
def get_best_sellers():
    # GET and determine the best sellers in the last 30 days
    # Get today's date
    today = datetime.today()

    # Subtract 30 daysjson
    thirty_days_ago = today - timedelta(days=30)
    
    # Optional: format the date as a string
    # thirty_days_ago_date = thirty_days_ago.strftime('%Y-%m-%d')
    sale_list_30_days = app_tables.sales_log.search(
        sale_date=q.greater_than_or_equal_to(thirty_days_ago)
    )

    # AGGREGATE sales by plant
    plant_sales = {}
    for sale in sale_list_30_days:
        plant    = sale['plant_sold']
        quantity = sale['quantity_sold']

        if plant:
            plant_name = plant['name']
            unit_price = plant['price'] if plant['price'] else 0
            total_sale = quantity * unit_price
            
            if plant_name in plant_sales:
                plant_sales[plant_name]['total_quantity'] += quantity
                plant_sales[plant_name]['total_sales']    += total_sale
            else:
                plant_sales[plant_name]    = {
                    'total_quantity' : quantity,
                    'total_sales'    : total_sale,
                    'unit_price'     : unit_price
                }

    # CONVERT to sorted list of dicts
    sort_sales = sorted(
        [
            {
                'plant_name'  : name,
                'total_sold'  : sale_data['total_quantity'],
                'unit_price'  : f"{sale_data['unit_price']:.2f}",
                'total_sales' : round(sale_data['total_sales'], 2)
            }
            for name, sale_data in plant_sales.items()
        ],
        key = lambda x: x['total_sales'],
        reverse = True
    )
    
    return sort_sales if sort_sales else False
    
@anvil.server.callable
def download_best_sellers_json():
    data = get_best_sellers()
    json_str = json.dumps(data, indent=4)
    return BlobMedia("application/json", json_str.encode('utf-8'), name="best_sellers.json")

@anvil.server.callable
def download_best_sellers_csv():
    data = get_best_sellers()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["plant_name", "total_quantity_sold", "total_sales_amount"])
    writer.writeheader()
    writer.writerows(data)
    return BlobMedia("text/csv", output.getvalue().encode('utf-8'), name="best_sellers.csv")

@anvil.server.callable
def download_best_sellers_pdf():
    data = get_best_sellers()
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 12)
    y = height - 50
    c.drawString(50, y, "Best Sellers Report")
    y -= 30

    for item in data:
        line = f"{item['plant_name']}(${item['unit_price']:.2f}): {item['total_quantity_sold']} sold, ${item['total_sales_amount']:.2f}"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return BlobMedia("application/pdf", buffer.getvalue(), name="best_sellers.pdf")

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

