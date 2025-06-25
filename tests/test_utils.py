from app.utils import normalize_question

def test_normalize_question_basic():
    assert normalize_question("is this a test?") == "Is this a test"
    assert normalize_question("  hello world??  ") == "Hello world"
    assert normalize_question("Already Normalized") == "Already Normalized"
    assert normalize_question("multiple???") == "Multiple"
    assert normalize_question("  spaced out question ? ") == "Spaced out question "
