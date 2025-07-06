import numpy as np
import statsmodels.api as sm

from app.llm.pipelines import PIPELINES


def get_param_lists():
    param_set = set()
    for pipeline in PIPELINES.values():
        param_set.update(pipeline.keys())
    param_set.discard("probability")
    param_list = sorted(param_set)
    return param_list


def get_categorical_params(param_list):
    categorical_params = {}
    for p in param_list:
        values = set()
        for pipeline in PIPELINES.values():
            v = pipeline.get(p, 0)
            if isinstance(v, str):
                values.add(v)
        if values:
            categorical_params[p] = sorted(values)
    return categorical_params


def get_feature_names(param_list, categorical_params):
    feature_names = []
    for p in param_list:
        if p in categorical_params:
            values = categorical_params[p]
            if len(values) == 2:
                val1, val2 = values
                feature_names.append(f"{p}={val2}")
            else:
                for val in values[1:]:
                    feature_names.append(f"{p}={val}")
        else:
            feature_names.append(p)
    return feature_names


def get_ohe_map(param_list, categorical_params):
    ohe_map = {}
    for p in param_list:
        if p in categorical_params:
            values = categorical_params[p]
            if len(values) == 2:
                val1, val2 = values
                ohe_map[p] = [(val2, f"{p}={val2}")]
            else:
                ohe_map[p] = []
                for val in values[1:]:
                    ohe_map[p].append((val, f"{p}={val}"))
    return ohe_map


def build_X_y(docs, param_list, categorical_params, ohe_map):
    X = []
    y = []
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
    return X, y


def calculate_logistic_analytics(docs):
    if not docs:
        return {"baseline_td_rate": None, "intercept": None, "effects": []}
    param_list = get_param_lists()
    categorical_params = get_categorical_params(param_list)
    feature_names = get_feature_names(param_list, categorical_params)
    ohe_map = get_ohe_map(param_list, categorical_params)
    X, y = build_X_y(docs, param_list, categorical_params, ohe_map)
    if not X or not y:
        return {"baseline_td_rate": None, "intercept": None, "effects": []}
    X = np.array(X)
    y = np.array(y)
    # Add intercept
    X = sm.add_constant(X)
    param_names = ["Intercept"] + feature_names

    model = sm.Logit(y, X)
    result = model.fit(disp=0)
    effects = result.params
    conf = result.conf_int(alpha=0.05)
    pvalues = result.pvalues

    intercept = float(effects[0])
    baseline_td_rate = 1 / (1 + np.exp(-intercept))

    effect_list = []
    for i, name in enumerate(param_names):
        if name == "Intercept":
            continue  # handled separately
        # Non-log effect: change in TD rate if this parameter is set to 1
        td_rate_with_param = 1 / (1 + np.exp(-(intercept + float(effects[i]))))
        delta_td_rate = td_rate_with_param - baseline_td_rate
        # Delta TD 95% CI: transform logit CI to probability CI
        td_rate_ci_low = 1 / (1 + np.exp(-(intercept + float(conf[i, 0]))))
        td_rate_ci_high = 1 / (1 + np.exp(-(intercept + float(conf[i, 1]))))
        delta_td_rate_ci_low = td_rate_ci_low - baseline_td_rate
        delta_td_rate_ci_high = td_rate_ci_high - baseline_td_rate
        effect_list.append(
            {
                "parameter": name,
                "effect": float(effects[i]),
                "ci_low": float(conf[i, 0]),
                "ci_high": float(conf[i, 1]),
                "p_value": float(pvalues[i]),
                "delta_td_rate": delta_td_rate,
                "delta_td_rate_ci_low": delta_td_rate_ci_low,
                "delta_td_rate_ci_high": delta_td_rate_ci_high,
            }
        )
    return {"baseline_td_rate": baseline_td_rate, "intercept": intercept, "effects": effect_list}
