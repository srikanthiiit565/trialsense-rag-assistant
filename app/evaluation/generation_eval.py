"""Generation evaluation utilities."""
from langchain_ollama import ChatOllama
from app.utils.config import settings


llm = ChatOllama(

    model=settings.OLLAMA_MODEL,

    base_url=settings.OLLAMA_BASE_URL,

    temperature=0

)



def keyword_score(

        answer,

        keywords

):

    answer = answer.lower()


    matched = 0


    for word in keywords:

        if word.lower() in answer:

            matched += 1


    return matched / len(keywords)




def evaluate_generation(

        answer,

        expected_keywords

):


    score = keyword_score(

        answer,

        expected_keywords

    )


    return {


        "keyword_grounding":

        round(score,2)

    }