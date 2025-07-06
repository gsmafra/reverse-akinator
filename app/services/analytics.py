from app.db_access.served_answers import get_all_served_answers


def compute_monolithic_analytics(docs):
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
    z = 1.96  # 95% confidence
    for pipeline, stats in pipeline_stats.items():
        num_answers = stats["num_answers"]
        num_thumbs_down = stats["num_thumbs_down"]
        if num_answers > 0:
            p = num_thumbs_down / num_answers
            se = (p * (1 - p) / num_answers) ** 0.5
            ci_low = max(0.0, p - z * se)
            ci_high = min(1.0, p + z * se)
        else:
            p = 0.0
            ci_low = 0.0
            ci_high = 0.0
        analytics.append(
            {
                "pipeline_name": pipeline,
                "num_thumbs_down": num_thumbs_down,
                "num_answers": num_answers,
                "ratio_thumbs_down": p,
                "ratio_thumbs_down_ci_low": ci_low,
                "ratio_thumbs_down_ci_high": ci_high,
            }
        )
    return analytics


def get_monolithic_analytics(db):
    docs = get_all_served_answers(db)
    return compute_monolithic_analytics(docs)
