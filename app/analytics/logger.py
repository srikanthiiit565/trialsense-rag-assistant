import json

from app.analytics.database import (
    get_connection
)



def log_query(

    query,
    answer,
    citations,
    latency,
    model,
    success=True

):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT INTO query_logs
        (
            query,
            answer,
            citations,
            latency,
            source_count,
            model,
            success
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (

            query,

            answer,

            json.dumps(citations),

            latency,

            len(citations),

            model,

            success

        )

    )


    conn.commit()

    conn.close()