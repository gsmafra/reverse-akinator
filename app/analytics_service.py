from app.db_access.served_answers import get_all_served_answers


def get_pipeline_analytics(db):
    docs = get_all_served_answers(db)

    pipeline_stats = {}
    for data in docs:
        pipeline = data.get("pipeline_id", data.get("pipeline_name", "unknown"))
        thumbs_down = data.get("thumbs_down", False)

        if pipeline not in pipeline_stats:
            pipeline_stats[pipeline] = {"num_thumbs_down": 0, "num_answers": 0}

        pipeline_stats[pipeline]["num_answers"] += 1
        if thumbs_down:
            pipeline_stats[pipeline]["num_thumbs_down"] += 1

    analytics = []
    for pipeline, stats in pipeline_stats.items():
        num_answers = stats["num_answers"]
        num_thumbs_down = stats["num_thumbs_down"]
        analytics.append(
            {
                "pipeline_name": pipeline,
                "num_thumbs_down": num_thumbs_down,
                "num_answers": num_answers,
                "ratio_thumbs_down": num_thumbs_down / num_answers,
            }
        )

    return analytics
