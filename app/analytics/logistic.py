import numpy as np
import statsmodels.api as sm

from app.llm.pipelines import PIPELINES


def calculate_logistic_analytics(docs):
    if not docs:
        return []

    # Use parameters from PIPELINES definitions
    param_set = set()
    for pipeline in PIPELINES.values():
        param_set.update(pipeline.keys())
    param_set.discard("probability")
    param_list = sorted(param_set)

    # Determine which params are categorical (string) and collect all possible values
    categorical_params = {}
    for p in param_list:
        values = set()
        for pipeline in PIPELINES.values():
            v = pipeline.get(p, 0)
            if isinstance(v, str):
                values.add(v)
        if values:
            categorical_params[p] = sorted(values)

    # Build X and y with smart OHE for categorical, numeric as-is
    X = []
    y = []
    feature_names = []
    ohe_map = {}  # param -> list of (val, col_name)
    for p in param_list:
        if p in categorical_params:
            values = categorical_params[p]
            if len(values) == 2:
                # Only one boolean column needed
                val1, val2 = values
                feature_names.append(f"{p}={val2}")
                ohe_map[p] = [(val2, f"{p}={val2}")]
            else:
                ohe_map[p] = []
                for val in values[1:]:  # drop first for reference
                    feature_names.append(f"{p}={val}")
                    ohe_map[p].append((val, f"{p}={val}"))
        else:
            feature_names.append(p)

    for d in docs:
        pipeline_id = d.get("pipeline_id", d.get("pipeline_name", "unknown"))
        pipeline_params = PIPELINES.get(pipeline_id, {})
        row = []
        for p in param_list:
            v = pipeline_params.get(p, 0)
            if p in categorical_params:
                values = categorical_params[p]
                if len(values) == 2:
                    # Only one boolean column for the second value
                    val1, val2 = values
                    row.append(1 if v == val2 else 0)
                else:
                    for val, _ in ohe_map[p]:
                        row.append(1 if v == val else 0)
            else:
                row.append(float(v))
        X.append(row)
        y.append(int(d.get("thumbs_down", False)))
    if not X or not y:
        return []
    X = np.array(X)
    y = np.array(y)
    # Add intercept
    X = sm.add_constant(X)
    param_names = ["Intercept"] + feature_names

    import math

    try:
        model = sm.Logit(y, X)
        result = model.fit(disp=0)
        effects = result.params
        conf = result.conf_int(alpha=0.05)
        pvalues = result.pvalues
    except Exception:
        print("Logistic regression failed, returning empty analytics.")
        return []

    analytics = []
    for i, name in enumerate(param_names):
        analytics.append(
            {
                "parameter": name,
                "effect": float(effects[i]),
                "ci_low": float(conf[i, 0]),
                "ci_high": float(conf[i, 1]),
                "p_value": float(pvalues[i]),
            }
        )
    return analytics
