from backend.ingestion.sources.youtube import extract_video_id


def test_bare_id():
    assert extract_video_id("ecmbMYIzNLs") == "ecmbMYIzNLs"


def test_id_with_trailing_junk():
    assert extract_video_id("ecmbMYIzNLs&list=RDecmbMYIzNLs&start_radio=1") == "ecmbMYIzNLs"


def test_full_url():
    assert extract_video_id("https://www.youtube.com/watch?v=ecmbMYIzNLs&t=10s") == "ecmbMYIzNLs"


def test_short_url():
    assert extract_video_id("https://youtu.be/ecmbMYIzNLs") == "ecmbMYIzNLs"