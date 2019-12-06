import sqlite3
from sqlite3 import Error

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

_SQL = {
    "get_endpoint_stats":
        """
            select
                name,
                endpoint_id,
                avg(result) as success_rate,
                avg(time) as average_time
            from endpoint
            where endpoint_id=?
        """
    ,
    "get_all_endpoint_stats":
        """
            select
                name,
                endpoint_id,
                avg(result) as success_rate,
                status_code,
                avg(time) as average_time
            from endpoint
            group by endpoint_id
        """
    ,
    "insert_test_results":
        """
        insert into endpoint(
            name,
            endpoint_id,
            result,
            status_code,
            time
        )
        values(?, ?, ?, ?, ?)
        """
    ,
}

def get_endpoint_stats(endpoint_id):
    conn = sqlite3.connect(r"hallmonitor.db")
    conn.row_factory = dict_factory

    cursor = conn.cursor()
    cursor.execute(_SQL['get_endpoint_stats'], (endpoint_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_all_endpoint_stats():
    conn = sqlite3.connect(r"hallmonitor.db")
    conn.row_factory = dict_factory

    cursor = conn.cursor()
    cursor.execute(_SQL['get_all_endpoint_stats'])
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def store_results(kwargs, res):
    conn = sqlite3.connect(r"hallmonitor.db")
    conn.row_factory = dict_factory

    name = f'/{kwargs.get("name")}'
    endpoint_id = sum([ord(x) for x in name])
    result = 1 if res.status_code==200 else 0
    params = (
        name,
        endpoint_id,
        result,
        res.status_code,
        res.elapsed.total_seconds(),
    )
    cursor = conn.cursor()
    cursor.execute(_SQL['insert_test_results'], params)
    cursor.close()
    conn.commit()
    conn.close()
    return
