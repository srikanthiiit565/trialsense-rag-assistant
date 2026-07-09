import requests
import streamlit as st
import time


# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

API_URL = "http://127.0.0.1:8000/query"


st.set_page_config(
    page_title="TrialSense AI",
    page_icon="🧬",
    layout="wide"
)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def call_backend(query):

    start_time = time.time()

    response = requests.post(
        API_URL,
        json={
            "query": query
        },
        timeout=120
    )

    latency = round(
        time.time() - start_time,
        2
    )

    result = response.json()

    result["latency"] = latency

    return result



def stream_text(text):

    """
    Simulates streaming response.
    """

    output = ""

    placeholder = st.empty()

    for word in text.split():

        output += word + " "

        placeholder.markdown(output)

        time.sleep(0.03)

    return output



# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("🧬 TrialSense AI")


    st.markdown(
        """
### Clinical Trial Intelligence Assistant

Powered by:

- LangGraph Agent
- ChromaDB
- Hybrid Retrieval
- Cross Encoder Reranker
- Llama 3.1
- Ollama
"""
    )


    st.divider()


    st.subheader(
        "Suggested Questions"
    )


    questions = [

        "What are Alzheimer's treatments?",

        "Compare Alzheimer's clinical trials",

        "List Phase III Alzheimer's trials",

        "Explain CAR-T therapy trials",

        "Find eligibility criteria for trials"

    ]


    for q in questions:

        if st.button(q):

            st.session_state.selected_question = q



# ---------------------------------------------------
# Main UI
# ---------------------------------------------------

st.title(
    "🧬 TrialSense AI"
)

st.caption(
    "Ask questions across millions of clinical research documents"
)


# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# ---------------------------------------------------
# User Input
# ---------------------------------------------------

query = st.chat_input(
    "Ask your research question..."
)


if "selected_question" in st.session_state:

    query = st.session_state.selected_question

    del st.session_state.selected_question



if query:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":query
        }
    )


    with st.chat_message("user"):

        st.markdown(query)



    with st.chat_message("assistant"):


        with st.spinner(
            "Searching clinical knowledge base..."
        ):


            try:

                result = call_backend(query)


                answer = result.get(
                    "answer",
                    ""
                )


                citations = result.get(
                    "citations",
                    []
                )


                latency = result.get(
                    "latency"
                )


                # -------------------------
                # Answer Streaming
                # -------------------------

                stream_text(answer)



                # -------------------------
                # Metrics
                # -------------------------

                st.divider()


                col1,col2,col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Response Time",
                        f"{latency}s"
                    )


                with col2:

                    st.metric(
                        "Sources Retrieved",
                        len(citations)
                    )


                with col3:

                    st.metric(
                        "Model",
                        "Llama 3.1"
                    )



                # -------------------------
                # Citations
                # -------------------------

                if citations:


                    st.divider()


                    st.subheader(
                        "📚 Evidence Sources"
                    )


                    for source in citations:

                        with st.expander(
                            f"Source: {source}"
                        ):

                            st.write(
                                "Document ID:"
                            )

                            st.code(
                                source
                            )

                            if source.startswith(
                                "NCT"
                            ):

                                st.markdown(
                                    f"""
ClinicalTrials.gov

https://clinicaltrials.gov/study/{source}
"""
                                )



                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )



            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )
                