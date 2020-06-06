import psycopg2
import numpy as np
import pandas as pd
from datetime import datetime


def query_data(query):
    conn = psycopg2.connect(host="localhost", port = 5432, database="covid_data", user="Xu", password="postgres")
    cur = conn.cursor()

    cur.execute(query)
    query_results = cur.fetchall()

    cur.close()
    conn.close()

    return query_results


def count_cases(query):
    data = query_data(query)
    data_dict = {}

    for d in data:
        name = d[1]
        if name in data_dict:
            data_dict[name] += 1
        else:
            data_dict[name] = 1

    return data_dict


def binary_search_tuples(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (high + low) // 2

        if arr[mid][1] < target:
            low = mid + 1
        elif arr[mid][1] > target:
            high = mid - 1
        else:
            return arr[mid]

    return arr[low] if abs(target - arr[low][1]) < abs(target - arr[high][1]) else arr[high]


def convert_to_datetime(dates, year):
    converted_dates = []
    for date in dates:
        split_date = date.split('/')
        split_date[-1] = year
        joined_date = '/'.join(split_date)
        converted_dates.append(datetime.strptime(joined_date, '%m/%d/%Y'))

    return converted_dates

# datetime format for start, end: month/day/year - ex: 3/1/20
def get_mobility_data(start, end):
    df = pd.read_csv('county_mobility_data.csv')
    start_date = start
    end_date = end
    county_mobility = {}

    for i in range(df.shape[0]):
        county = df.loc[i, 'region'].split(' ')
        county.pop()
        parsed_county = ' '.join(county)

        name = df.loc[i, 'sub-region'] + '-' + parsed_county
        mobility_data = np.array(df.loc[i, start_date:end_date])

        county_mobility[name] = np.nanmean(mobility_data)

    return county_mobility
