import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg.connect(
        host="localhost",
        port=5433,  # host port from docker-compose
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

if __name__ == "__main__":
    with get_conn() as conn:
        print(conn.execute("SELECT count(*) FROM sources").fetchone())