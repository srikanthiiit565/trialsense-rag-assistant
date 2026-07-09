from app.analytics.database import (
    get_connection
)



def get_metrics():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM query_logs
        """
    )

    total_queries = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT AVG(latency)
        FROM query_logs
        """
    )

    avg_latency = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM query_logs
        WHERE success = 0
        """
    )

    failures = cursor.fetchone()[0]


    conn.close()


    return {

        "total_queries":
            total_queries,

        "average_latency":
            round(avg_latency or 0,2),

        "failures":
            failures

    }