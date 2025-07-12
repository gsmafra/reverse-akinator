from app.analytics.logistic import calculate_logistic_analytics, PIPELINES


def test_logistic_basic_binary():
    # Use a dataset with three pipelines and all parameter combinations
    docs = [
        {"pipeline_id": "A", "thumbs_down": True},
        {"pipeline_id": "A", "thumbs_down": False},
        {"pipeline_id": "A", "thumbs_down": True},
        {"pipeline_id": "A", "thumbs_down": False},
        {"pipeline_id": "B", "thumbs_down": True},
        {"pipeline_id": "B", "thumbs_down": False},
        {"pipeline_id": "B", "thumbs_down": True},
        {"pipeline_id": "B", "thumbs_down": False},
        {"pipeline_id": "C", "thumbs_down": True},
        {"pipeline_id": "C", "thumbs_down": False},
        {"pipeline_id": "C", "thumbs_down": True},
        {"pipeline_id": "C", "thumbs_down": False},
    ]

    PIPELINES.clear()
    PIPELINES.update(
        {
            "A": {"model": "m1", "use_wikipedia": True},
            "B": {"model": "m2", "use_wikipedia": False},
            "C": {"model": "m1", "use_wikipedia": False},
        }
    )
    analytics = calculate_logistic_analytics(docs)
    effects = analytics["effects"]
    param_names = [a["parameter"] for a in effects]
    assert "intercept" in analytics
    assert "model=m2" in param_names
    assert "use_wikipedia" in param_names
    for a in effects:
        assert isinstance(a["effect"], float)
        assert isinstance(a["p_value"], float)


def test_logistic_multiclass_ohe():
    # Use a dataset with enough samples for each class
    docs = [
        {"pipeline_id": "A", "thumbs_down": True},
        {"pipeline_id": "A", "thumbs_down": False},
        {"pipeline_id": "B", "thumbs_down": False},
        {"pipeline_id": "B", "thumbs_down": True},
        {"pipeline_id": "C", "thumbs_down": True},
        {"pipeline_id": "C", "thumbs_down": False},
        {"pipeline_id": "C", "thumbs_down": False},
    ]

    PIPELINES.clear()
    PIPELINES.update(
        {
            "A": {"model": "m1"},
            "B": {"model": "m2"},
            "C": {"model": "m3"},
        }
    )
    analytics = calculate_logistic_analytics(docs)
    effects = analytics["effects"]
    param_names = [a["parameter"] for a in effects]
    assert "intercept" in analytics
    assert "model=m2" in param_names
    assert "model=m3" in param_names
    assert "model=m1" not in param_names


def test_logistic_empty():
    analytics = calculate_logistic_analytics([])
    assert set(analytics.keys()) == {"baseline_td_rate", "intercept", "effects"}
    assert analytics["effects"] == []
