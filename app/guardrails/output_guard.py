MEDICAL_DISCLAIMER = """

Note:
This response is based on published research
and clinical trial information.

It is not medical advice.
Consult qualified healthcare professionals
for diagnosis or treatment decisions.

"""



def apply_output_guardrail(
        answer
):


    unsafe_words = [

        "you should take",

        "you must take",

        "guaranteed cure",

        "100% effective"

    ]


    answer_lower = answer.lower()



    for word in unsafe_words:

        if word in answer_lower:

            answer = (

                "The information may require "
                "professional medical review.\n\n"
                + answer

            )


    return (

        answer +

        MEDICAL_DISCLAIMER

    )