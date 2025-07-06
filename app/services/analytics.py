from app.db_access.served_answers import get_all_served_answers
from app.analytics.logistic import calculate_logistic_analytics
from app.analytics.monolithic import compute_monolithic_analytics


def get_monolithic_analytics(db):
    docs = get_all_served_answers(db)
    return compute_monolithic_analytics(docs)


def get_logistic_analytics(db):
    docs = get_all_served_answers(db)
    return calculate_logistic_analytics(docs)
