from app.db_access import get_canonical_answer


class MockDoc:  # pylint: disable=too-few-public-methods
    def to_dict(self):
        return {"answer": "yes"}


class MockQuery:  # pylint: disable=too-few-public-methods
    def where(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self

    def get(self):
        return [MockDoc()]


class MockCollection:  # pylint: disable=too-few-public-methods
    def where(self, *args, **kwargs):  # pylint: disable=unused-argument
        return MockQuery()


class MockDB:  # pylint: disable=too-few-public-methods
    def collection(self, name):  # pylint: disable=unused-argument
        return MockCollection()


def test_get_cached_answer_returns_answer():
    mock_db = MockDB()
    result = get_canonical_answer(mock_db, "Mario", "Is he Italian?")
    assert result
