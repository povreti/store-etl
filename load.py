import sqlite3
import logging


def create_tables(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS sales')
    cursor.execute('DROP TABLE IF EXISTS categories')
    cursor.execute('DROP TABLE IF EXISTS location')

    cursor.execute('''
        CREATE TABLE location (
            location_id INTEGER PRIMARY KEY,
            postal_code TEXT,
            country TEXT,
            city TEXT,
            state TEXT,
            region TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category TEXT,
            sub_category TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE sales (
            sales_id INTEGER PRIMARY KEY,
            ship_mode TEXT,
            amount REAL,
            quantity INTEGER,
            discount REAL,
            profit REAL,
            segment TEXT,
            location_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (location_id) REFERENCES location(location_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')

    logging.info('Созданы 3 таблицы: location, categories, sales')
    connection.commit()
    connection.close()


def fill_tables(df, db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Заполнение location
    location = df[['Postal Code', 
                  'Country',
                  'City',
                  'State',
                  'Region']].drop_duplicates()
    location_data = list(location.itertuples(index=False, name=None))
    cursor.executemany(
        '''INSERT INTO location (
            postal_code,
            country,
            city,
            state,
            region
            ) VALUES (?, ?, ?, ?, ?)''',
        location_data
    )

    # Заполнение categories
    categories = df[['Category', 'Sub-Category']].drop_duplicates()
    categories_data = list(categories.itertuples(index=False, name=None))
    cursor.executemany(
        '''INSERT INTO categories (category, sub_category)
        VALUES (?, ?)''',
        categories_data
    )

    # Заполнение sales
    cursor.execute('SELECT * FROM location')
    location_ids = {
        (row[1], row[2], row[3], row[4], row[5]) : row[0]
        for row in cursor.fetchall()
    }

    cursor.execute('SELECT * FROM categories')
    category_ids = {
        (row[1], row[2]): row[0]
        for row in cursor.fetchall()
    }

    sales_data = []
    for row in df.itertuples(index=False, name=None):
        location_key = (
            str(row[5]),
            row[2],
            row[3],
            row[4],
            row[6]
        )

        category_key = (row[7], row[8]) # Sub-Category

        sales_data.append((
            row[0], 
            row[9],
            row[10],
            row[11],
            row[12],
            row[1],
            location_ids[location_key],
            category_ids[category_key]
        ))

    cursor.executemany(
        '''INSERT INTO sales (ship_mode,
            amount,
            quantity,
            discount,
            profit,
            segment,
            location_id,
            category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        sales_data
    )

    logging.info(
        f'\nТаблицы заполнены:\n'
        f'location ({len(location_data)} строк)\n'
        f'categories ({len(categories_data)} строк)\n'
        f'sales ({len(sales_data)} строк)\n'
    )

    connection.commit()
    connection.close()


def load_data(df, db_path):
    create_tables(db_path)
    fill_tables(df, db_path)