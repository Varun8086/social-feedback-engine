import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from backend.ingestion.models import RawPost
from backend.ingestion.sources.base import BaseSource


class YouTubeSource(BaseSource):
    def __init__(self, video_ids, max_pages=3):
        self.video_ids = video_ids
        self.max_pages = max_pages
        self.client = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])

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