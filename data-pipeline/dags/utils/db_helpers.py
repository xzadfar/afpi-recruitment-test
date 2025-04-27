from airflow.hooks.postgres_hook import PostgresHook

import psycopg2
from psycopg2.extras import execute_values

def run_query(query, conn_id, data=None):
    pg_hook = PostgresHook(postgres_conn_id=conn_id)
    conn = pg_hook.get_conn()

    cursor = conn.cursor()

    insert_query = query

    if(data is None):  
        cursor.execute(insert_query)
    else: 
        execute_values(cursor, insert_query, data)

    conn.commit()
    cursor.close()
    conn.close()

    print("Data inserted into PostgreSQL successfully.")