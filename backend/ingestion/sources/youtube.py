import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from backend.ingestion.models import RawPost
from backend.ingestion.sources.base import BaseSource
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta, timezone


def extract_video_id(value: str) -> str:
    """Accept a bare ID, a full URL, or an ID with trailing '&...' junk."""
    value = value.strip()
    if value.startswith("http"):
        u = urlparse(value)
        if u.hostname == "youtu.be":
            return u.path.lstrip("/")
        return parse_qs(u.query)["v"][0]
    return value.split("&")[0]

def pick_popular(items, min_views):
    """Keep videos with enough views AND comments enabled, most viewed first."""
    out = []
    for it in items:
        stats = it.get("statistics", {})
        views = int(stats.get("viewCount", 0))
        comments = int(stats.get("commentCount", 0))
        if views >= min_views and comments > 0:
            out.append((it["id"], views))
    out.sort(key=lambda x: -x[1])
    return [vid for vid, _ in out]

class YouTubeSource(BaseSource):
    def __init__(self, video_ids, max_pages=3):
        self.video_ids = [extract_video_id(v) for v in video_ids]
        self.max_pages = max_pages
        self.client = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])

    def discover(self, queries, min_views=25_000, days=90, per_query=50):
        since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        found = []
        for q in queries:
            resp = self.client.search().list(
                part="id", q=q, type="video", order="viewCount",
                publishedAfter=since, maxResults=per_query,
            ).execute()
            found.extend(i["id"]["videoId"] for i in resp["items"])
        found = list(dict.fromkeys(found))  # dedupe, keep order

        items = []
        for i in range(0, len(found), 50):  # videos.list accepts 50 ids max
            resp = self.client.videos().list(
                part="statistics", id=",".join(found[i:i + 50])
            ).execute()
            items.extend(resp["items"])

        self.video_ids = pick_popular(items, min_views)
        return self.video_ids
    
    def fetch(self):
        posts = []
        for vid in self.video_ids:
            try:
                posts.extend(self._fetch_video(vid))
            except HttpError as e:
                print(f"skipping {vid}: {e.status_code}")  # e.g. comments disabled
        return posts


    
    def _fetch_video(self, video_id):
        posts, token = [], None
        for _ in range(self.max_pages):
            resp = self.client.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=100,
                order="time", textFormat="plainText", pageToken=token,
            ).execute()
            for item in resp["items"]:
                s = item["snippet"]["topLevelComment"]["snippet"]
                posts.append(RawPost(
                    platform="youtube",
                    source_external_id=video_id,
                    external_id=item["id"],
                    body=s["textDisplay"],
                    posted_at=datetime.fromisoformat(s["publishedAt"]),
                    author=s.get("authorDisplayName"),
                    url=f"https://www.youtube.com/watch?v={video_id}&lc={item['id']}",
                    score=s.get("likeCount"),
                ))
            token = resp.get("nextPageToken")
            if not token:
                break
        return posts

    