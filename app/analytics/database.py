import sqlite3
from pathlib import Path


DB_PATH = Path("data/trialsense_analytics.db")


def get_connection():

    DB_PATH.parent.mkdir(
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    return conn



def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS query_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            query TEXT,

            answer TEXT,

            citations TEXT,

            latency REAL,

            source_count INTEGER,

            model TEXT,

            success BOOLEAN,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    conn.commit()

    conn.close()



if __name__ == "__main__":

    initialize_database()

    print(
        "Analytics database initialized"
    )