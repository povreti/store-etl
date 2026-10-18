import logging
import sqlite3


def sales_by_category(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT category, SUM(sales.amount) AS amount_sum FROM categories
        JOIN sales ON sales.category_id = categories.category_id
        GROUP BY category ORDER BY amount_sum DESC
    ''')
    result = cursor.fetchall()

    logging.info('Продажи по категориям:')
    for category, sales in result:
        logging.info(f'{category}: {sales:,.2f}')
    logging.info('\n')

    connection.close()


def profit_by_region(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT region, SUM(sales.profit) as sum_profit FROM location
        JOIN sales ON location.location_id = sales.location_id
        GROUP BY region ORDER BY sum_profit DESC
    ''')

    logging.info('Прибыль по регионам:')
    for region, profit in cursor.fetchall():
        logging.info(f'{region}: {profit:,.2f}')
    logging.info('\n')

    connection.close()


def top_cities_by_sales(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT city, SUM(sales.amount) AS sum_amount FROM location
        JOIN sales ON sales.location_id = location.location_id
        GROUP BY city ORDER BY sum_amount DESC LIMIT 10
    ''')

    logging.info('Топ-10 городов по продажам:')
    for city, amount in cursor.fetchall():
        logging.info(f'{city}: {amount:,.2f}')
    logging.info('\n')

    connection.close()


def unprofitable_sub_categories(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT sub_category, SUM(profit) AS sum_profit FROM categories
        JOIN sales ON sales.category_id = categories.category_id
        GROUP BY sub_category HAVING sum_profit < 0
        ORDER BY sum_profit
    ''')

    logging.info('Убыточные подкатегории:')
    for sub_category, profit in cursor.fetchall():
        logging.info(f'{sub_category}: убыток {profit:,.2f}')
    logging.info('\n')

    connection.close()


def report_data(db_path):
    sales_by_category(db_path)
    profit_by_region(db_path)
    top_cities_by_sales(db_path)
    unprofitable_sub_categories(db_path)