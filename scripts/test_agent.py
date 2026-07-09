from app.agents.rag_agent import RAGAgent


def main():
    agent = RAGAgent()

    result = agent.ask(

        "What are the latest Alzheimer's treatments?"

    )

    print()

    print("=" * 80)

    print(result["answer"])

    print()

    print("=" * 80)

    print("Citations")

    print("=" * 80)

    for citation in result["citations"]:

        print(citation)


    # Helpful note when testing fallback behavior
    if os.getenv("GROQ_FORCE_FAIL"):
        print('\n[GROQ_FORCE_FAIL is set — test forced Groq failure/fallback]\n')


if __name__ == "__main__":
    main()
