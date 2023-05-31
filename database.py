import psycopg2

class Database:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def create_schema(self):
        self.connect()
        self.cursor.execute('''
            CREATE SCHEMA IF NOT EXISTS real_estate;
        ''')
        self.connection.commit()
        self.disconnect()

    def create_table(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id SERIAL PRIMARY KEY,
                real_estate_name TEXT,
                group_type TEXT,
                category_type TEXT,
                property_price NUMERIC(15, 2),
                property_name TEXT,
                city_name TEXT,
                abbreviation_uf TEXT,
                neighborhood_name TEXT,
                address TEXT,
                bedrooms_number INTEGER,
                suites_number INTEGER,
                car_vacancies_number INTEGER,
                property_area_size NUMERIC(15, 2),
                private_property_area NUMERIC(15, 2),
                furniture TEXT,
                floor TEXT
            );
        ''')
        self.connection.commit()
        self.disconnect()

    def insert(self, real_estate_name, group_type, category_type, property_price, property_name, city_name, abbreviation_uf, neighborhood_name, address, bedrooms_number, suites_number, car_vacancies_number, property_area_size, private_property_area, furniture, floor):
        self.connect()
        self.cursor.execute('''
            INSERT INTO properties (real_estate_name, group_type, category_type, property_price, property_name, city_name, abbreviation_uf, neighborhood_name, address, bedrooms_number, suites_number, car_vacancies_number, property_area_size, private_property_area, furniture, floor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (real_estate_name, group_type, category_type, property_price, property_name, city_name, abbreviation_uf, neighborhood_name, address, bedrooms_number, suites_number, car_vacancies_number, property_area_size, private_property_area, furniture, floor))
        self.connection.commit()
        self.disconnect()
