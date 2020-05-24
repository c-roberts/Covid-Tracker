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