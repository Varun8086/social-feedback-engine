from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawPost:
    platform: str            # 'youtube' | 'reddit' | 'hackernews'
    source_external_id: str  # video id / subreddit name
    external_id: str         # the platform's own post/comment id
    body: str
    posted_at: datetime
    author: str | None = None
    title: str | None = None
    url: str | None = None
    score: int | None = None