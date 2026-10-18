import logging
import extract
import transform
import load
import checks
import reports


csv_path = 'Data/store.csv'
db_path = 'Data/store.db'


logging.basicConfig(
    filename='Logs/report.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s %(message)s'
)


if __name__ == '__main__':
    df = extract.extract_data(csv_path)
    df = transform.transform_data(df)
    load.load_data(df, db_path)
    checks.check_data(db_path)
    reports.report_data(db_path)