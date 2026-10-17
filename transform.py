import logging


def delete_duplicates(df):
    qty_duplicates = df.duplicated().sum()
    logging.info(f'Удалено {qty_duplicates} дубликатов\n')
    df = df[~df.duplicated()]
    return df


def transform_data(df):
    df = delete_duplicates(df)
    return df