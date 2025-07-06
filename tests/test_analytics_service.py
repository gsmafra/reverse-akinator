import math

from app.services.analytics import compute_monolithic_analytics


def test_compute_pipeline_analytics_basic():
    docs = [
        {"pipeline_id": "A", "thumbs_down": True},
        {"pipeline_id": "A", "thumbs_down": False},
        {"pipeline_id": "A", "thumbs_down": True},
        {"pipeline_id": "B", "thumbs_down": False},
        {"pipeline_id": "B", "thumbs_down": False},
    ]
    analytics = compute_monolithic_analytics(docs)
    # Convert to dict for easy lookup
    result = {a["pipeline_name"]: a for a in analytics}

    # Pipeline A: 2 thumbs down, 3 answers
    a = result["A"]
    assert a["num_thumbs_down"] == 2
    assert a["num_answers"] == 3
    assert math.isclose(a["ratio_thumbs_down"], 2 / 3)
    # Confidence interval should be within [0,1]
    assert 0.0 <= a["ratio_thumbs_down_ci_low"] <= a["ratio_thumbs_down"] <= a["ratio_thumbs_down_ci_high"] <= 1.0

    # Pipeline B: 0 thumbs down, 2 answers
    b = result["B"]
    assert b["num_thumbs_down"] == 0
    assert b["num_answers"] == 2
    assert b["ratio_thumbs_down"] == 0.0
    assert b["ratio_thumbs_down_ci_low"] == 0.0
    assert b["ratio_thumbs_down_ci_high"] >= 0.0


def test_compute_pipeline_analytics_empty():
    docs = []
    analytics = compute_monolithic_analytics(docs)
    assert not analytics
