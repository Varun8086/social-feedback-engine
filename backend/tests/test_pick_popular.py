from backend.ingestion.sources.youtube import pick_popular


def test_pick_popular_filters_views_and_comments():
    items = [
        {"id": "a", "statistics": {"viewCount": "50000", "commentCount": "10"}},
        {"id": "b", "statistics": {"viewCount": "1000", "commentCount": "10"}},
        {"id": "c", "statistics": {"viewCount": "90000"}},  # comments disabled
    ]
    assert pick_popular(items, 25_000) == ["a"]