from app.guardrails.input_guard import (
    input_guard
)

from app.guardrails.retrieval_guard import (
    validate_context
)

from app.guardrails.output_guard import (
    apply_output_guardrail
)




def check_input(query):

    return input_guard(query)



def check_retrieval(documents):

    return validate_context(documents)



def check_output(answer):

    return apply_output_guardrail(answer)