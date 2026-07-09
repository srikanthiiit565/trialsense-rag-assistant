import re



INJECTION_PATTERNS = [

    "ignore previous instructions",

    "ignore system prompt",

    "reveal your prompt",

    "show system message",

    "jailbreak"

]




def detect_prompt_injection(
        query: str
):

    query_lower = query.lower()


    for pattern in INJECTION_PATTERNS:

        if pattern in query_lower:

            return False, (
                "Potential prompt injection detected"
            )


    return True, query




def mask_pii(
        text:str
):

    # Email masking

    text = re.sub(

        r'\S+@\S+',

        "[EMAIL_REMOVED]",

        text

    )


    # Phone masking

    text = re.sub(

        r'\b\d{10}\b',

        "[PHONE_REMOVED]",

        text

    )


    return text




def input_guard(query):


    safe, message = (
        detect_prompt_injection(query)
    )


    if not safe:

        return {

            "allowed":False,

            "message":message

        }


    cleaned = mask_pii(query)



    return {

        "allowed":True,

        "query":cleaned

    }