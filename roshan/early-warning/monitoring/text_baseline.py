"""Train-only TF-IDF/logistic regression transcript baseline."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from monitoring.inputs import render_monitor_input


class TextBaseline:
    def __init__(self, seed=0):
        self.pipeline = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=20000, sublinear_tf=True),
            LogisticRegression(C=1.0, max_iter=2000, random_state=seed),
        )

    def fit(self, rows):
        labels = [int(r['eventual_unauthorized_attempt']) for r in rows]
        if len(set(labels)) != 2:
            raise ValueError('Text baseline requires both outcome classes in training data')
        self.pipeline.fit([render_monitor_input(r) for r in rows], labels)
        return self

    def predict(self, rows):
        return self.pipeline.predict_proba([render_monitor_input(r) for r in rows])[:, 1]
