from app.gemini import _parse_gemini_response  # Import the function
from dot_dict import DotDict


def test_valid_response_yes():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "Yes"}]}}]})
    assert _parse_gemini_response(response) == "yes"


def test_valid_response_no():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "No"}]}}]})
    assert _parse_gemini_response(response) == "no"


def test_valid_response_ambiguous():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "amb"}]}}]})
    assert _parse_gemini_response(response) == "ambiguous"


def test_valid_response_with_extra_whitespace():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "  Yes  "}]}}]})
    assert _parse_gemini_response(response) == "yes"


def test_no_response():
    response = None
    assert _parse_gemini_response(response) == "No response from the model"
    response = DotDict({})
    assert _parse_gemini_response(response) == "No response from the model"


def test_no_candidates():
    response = DotDict({"candidates": []})
    assert _parse_gemini_response(response) == "No response from the model"


def test_no_content():
    response = DotDict({"candidates": [{"content": None}]})
    assert _parse_gemini_response(response) == "No content in the first candidate"
    response = DotDict({"candidates": [{"content": None}]})
    assert _parse_gemini_response(response) == "No content in the first candidate"
    response = DotDict({"candidates": [{"content": {}}]})
    assert _parse_gemini_response(response) == "No content in the first candidate"


def test_no_parts():
    response = DotDict({"candidates": [{"content": {"parts": None}}]})
    assert _parse_gemini_response(response) == "No content parts in the first candidate"


def test_invalid_answer_format():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "invalid"}]}}]})
    assert _parse_gemini_response(response) == "Invalid answer format: 'invalid'"


def test_empty_text():
    response = DotDict({"candidates": [{"content": {"parts": [{"text": "Please Provide"}]}}]})
    assert _parse_gemini_response(response) == "Invalid answer format: 'Please Provide'"
