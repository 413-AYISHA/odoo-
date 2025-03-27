import csv
import xmlrpc.client

# Odoo Server Details
URL = 'http://10.10.192.198:8069'
DB = 'demo'
USERNAME = 'jacky@gmail.com'
PASSWORD = 'ayisha'

# Connect to Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))

# CSV File Path
file_path = '/home/ayisha/Downloads/bank_data/bank_data.csv'

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        bank_name = row.get('BANK')
        branch_name = row.get('BRANCH')
        ifsc_code = row.get('IFSC')
        
        if not (bank_name and branch_name and ifsc_code):
            print(f"Skipping row due to missing data: {row}")
            continue
        
        # Search for existing bank
        bank_ids = models.execute_kw(DB, uid, PASSWORD, 'hr.bank', 'search', [[('name', '=', bank_name)]])
        
        if bank_ids:
            bank_id = bank_ids[0]
        else:
            bank_id = models.execute_kw(DB, uid, PASSWORD, 'hr.bank', 'create', [{'name': bank_name}])
        
        # Create Branch
        branch_id = models.execute_kw(DB, uid, PASSWORD, 'hr.bank.branch', 'create', [{
            'name': branch_name,
            'bank_id': bank_id,
            'ifsc_code': ifsc_code
        }])
        print(f"Imported branch {branch_name} under bank {bank_name}")

print("CSV Import Completed")

