import os
import csv
from database import Database
from dotenv import load_dotenv

CURRDIR = os.path.dirname(__file__)

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_DATABASE')
port = os.getenv('DB_PORT')

db = Database(host, user, password, dbname, port)

db.create_schema()
db.create_table()

def process_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            print(row)
            # db.insert(
            #     row['real_estate_name'],
            #     row['group_type'],
            #     row['category_type'],
            #     row['property_price'],
            #     row['property_name'],
            #     row['city_name'],
            #     row['abbreviation_uf'],
            #     row['neighborhood_name'],
            #     row['address'],
            #     row['bedrooms_number'],
            #     row['suites_number'],
            #     row['car_vacancies_number'],
            #     row['property_area_size'],
            #     row['private_property_area'],
            #     row['furniture'],
            #     row['floor']
            # )

    db.disconnect()


file_path = os.path.join(CURRDIR, 'data/real_estate_data.csv')

process_csv(file_path)