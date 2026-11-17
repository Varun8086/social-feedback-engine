import os

from transformers import pipeline

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
BATCH_SIZE = int(os.getenv("SENTIMENT_BATCH_SIZE", "8"))
MAX_LEN = int(os.getenv("SENTIMENT_MAX_LEN", "256"))
_clf = None


def get_classifier():
    global _clf
    if _clf is None:  # load once, reuse (loading is slow)
        _clf = pipeline("sentiment-analysis", model=MODEL)
    return _clf


def score_texts(texts):
    """Return a list of (label, confidence) for each text."""
    safe = [t.strip() or "." for t in texts]  # model can't take empty strings
    out = get_classifier()(
        safe, truncation=True, max_length=MAX_LEN, batch_size=BATCH_SIZE
    )
    return [(r["label"].lower(), r["score"]) for r in out]