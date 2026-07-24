from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound


yt_api = YouTubeTranscriptApi()


def fetch_transcript(video_id):

    try:
        transcript = yt_api.fetch(
            video_id,
            languages=["en"]
        )

        print("Using English transcript")

    except NoTranscriptFound:

        transcript = yt_api.fetch(
            video_id,
            languages=["hi"]
        )

        print("Using Hindi transcript")

    return transcript