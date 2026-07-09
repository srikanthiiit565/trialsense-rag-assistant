from app.evaluation.dataset import (
    load_dataset
)

from app.evaluation.retrieval_eval import (
    evaluate_retrieval
)


from app.evaluation.generation_eval import (
    evaluate_generation
)



def run():


    dataset = load_dataset()



    print(
        "\n=============================="
    )

    print(
        "TrialSense AI Evaluation"
    )

    print(
        "==============================\n"
    )



    retrieval_results = (
        evaluate_retrieval(dataset)
    )


    total_recall = sum(

        x["recall"]

        for x in retrieval_results

    ) / len(retrieval_results)



    print(
        "Retrieval Recall@5:",
        round(total_recall,2)
    )



    print(
        "\nGeneration Evaluation"
    )


    for item in dataset:


        # Demo answer
        # In production:
        # call LangGraph pipeline

        answer = """

        Alzheimer's treatments include
        donepezil, memantine,
        and anti-amyloid therapies.

        """



        score = evaluate_generation(

            answer,

            item["expected_keywords"]

        )


        print(

            item["question"]

        )


        print(

            score

        )



if __name__ == "__main__":

    run()