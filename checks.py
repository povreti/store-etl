import logging
import sqlite3

def check_row_count(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM location')
    qty_location = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM categories')
    qty_categories = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM sales')
    qty_sales = cursor.fetchone()[0]

    logging.info(f'''
        При проверке данных выявлено следующее количество записей:
        location - {qty_location}
        categories - {qty_categories}
        sales - {qty_sales}\n
    ''')

    connection.close()


def check_duplicates(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for table, columns in {
        'location': 'postal_code, country, city, state, region',
        'categories': 'category, sub_category'
    }.items():
        cursor.execute(f'''
            SELECT COUNT(*) FROM (
            SELECT {columns} FROM {table}
            GROUP BY {columns} HAVING COUNT(*) > 1
            )
        ''')
        duplicates = cursor.fetchone()[0]
        logging.info(f'{table}: обнаружено дубликатов: {duplicates}')
    
    logging.info('\n')
    connection.close()


def check_nulls(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for table in ['location', 'categories', 'sales']:
        cursor.execute(f'PRAGMA table_info({table})')
        columns = [row[1] for row in cursor.fetchall()]
        nulls = 0
        for column in columns:
            cursor.execute(f'''
                SELECT COUNT(*) FROM {table} WHERE {column} IS NULL
            ''')
            nulls += cursor.fetchone()[0]
        logging.info(f'{table}: {nulls} пустых значений')
    
    logging.info('\n')
    connection.close()


def check_foreign_keys(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_key_check')
    errors = cursor.fetchall()

    logging.info(f'Найдено нарушений внешних ключей: {len(errors)}')

    connection.close()


def check_data(db_path):
    check_row_count(db_path)
    check_duplicates(db_path)
    check_nulls(db_path)
    check_foreign_keys(db_path)