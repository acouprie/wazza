import psycopg2
import os

def get_conn(app):
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DB'),
    )
    app.state.conn = conn
    return conn

def close_conn(app):
    conn = app.state.conn
    conn.close()