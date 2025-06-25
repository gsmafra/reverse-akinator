def normalize_question(question):
    question = question.strip()
    question = question[0].upper() + question[1:]
    while question.endswith("?"):
        question = question[:-1]
    return question
