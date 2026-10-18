import pandas as pd


def extract_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError('Файл по заданому пути не найден')
    except pd.errors.EmptyDataError:
        raise ValueError('Файл пустой')