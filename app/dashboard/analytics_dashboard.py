import streamlit as st
import pandas as pd
import sqlite3


DB_PATH = (
    "data/trialsense_analytics.db"
)


st.set_page_config(

    page_title="TrialSense Analytics",

    page_icon="📊",

    layout="wide"

)


st.title(
    "📊 TrialSense AI Analytics Dashboard"
)


conn = sqlite3.connect(
    DB_PATH
)



df = pd.read_sql_query(

    """
    SELECT *
    FROM query_logs
    ORDER BY timestamp DESC

    """,

    conn

)


conn.close()



if df.empty:

    st.warning(
        "No queries logged yet"
    )

    st.stop()



# --------------------------
# KPI Cards
# --------------------------


col1,col2,col3 = st.columns(3)



with col1:

    st.metric(

        "Total Queries",

        len(df)

    )



with col2:

    st.metric(

        "Average Latency",

        f"{df.latency.mean():.2f}s"

    )



with col3:

    success_rate = (
        df.success.mean()*100
    )

    st.metric(

        "Success Rate",

        f"{success_rate:.1f}%"

    )


st.divider()



# --------------------------
# Latency Chart
# --------------------------


st.subheader(
    "Latency Trend"
)


st.line_chart(

    df["latency"]

)



# --------------------------
# Query Analysis
# --------------------------


st.subheader(
    "Recent Questions"
)


st.dataframe(

    df[
        [
            "query",
            "source_count",
            "latency",
            "timestamp"
        ]
    ],

    use_container_width=True

)