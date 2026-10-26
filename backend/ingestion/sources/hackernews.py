import html
import re
from datetime import datetime

import requests

from backend.ingestion.models import RawPost
from backend.ingestion.sources.base import BaseSource

URL = "https://hn.algolia.com/api/v1/search_by_date"


def clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)       # strip tags
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


class HackerNewsSource(BaseSource):
    def __init__(self, queries, max_pages=3):
        self.queries = queries
        self.max_pages = max_pages

    def fetch(self):
        posts = []
        for q in self.queries:
            for page in range(self.max_pages):
                r = requests.get(
                    URL,
                    params={"query": q, "tags": "comment",
                            "hitsPerPage": 100, "page": page},
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()
                for hit in data["hits"]:
                    body = clean_html(hit.get("comment_text") or "")
                    if not body:
                        continue
                    posts.append(RawPost(
                        platform="hackernews",
                        source_external_id=q,
                        external_id=hit["objectID"],
                        body=body,
                        posted_at=datetime.fromisoformat(hit["created_at"]),
                        author=hit.get("author"),
                        title=hit.get("story_title"),
                        url=f"https://news.ycombinator.com/item?id={hit['objectID']}",
                    ))
                if page >= data["nbPages"] - 1:
                    break
        return posts