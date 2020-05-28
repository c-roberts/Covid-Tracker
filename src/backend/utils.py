import psycopg2


def query_data(query):
    conn = psycopg2.connect(host="localhost", port = 5432, database="covid_data", user="Xu", password="postgres")
    cur = conn.cursor()

    cur.execute(query)
    query_results = cur.fetchall()

    cur.close()
    conn.close()

    return query_results


def count_cases_by_state(query):
    data = query_data(query)
    states_data = {}

    for d in data:
        state = d[1]
        if state in states_data:
            states_data[state] += 1
        else:
            states_data[state] = 1

    return states_data


def binary_search_tuples(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (high + low) // 2

        if arr[mid][1] < x:
            low = mid + 1
        elif arr[mid][1] > x:
            high = mid - 1
        else:
            return arr[mid]

    return arr[low] if abs(x - arr[low][1]) < abs(x - arr[high][1]) else arr[high]
