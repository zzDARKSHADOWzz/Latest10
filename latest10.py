import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

# Set the YouTube API key
YOUTUBE_API_KEY = "YOUR_API_KEY"

def get_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    video_id = None
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        video_id = youtube_regex_match.group(6)

    return video_id

def get_video_comments(video_id):
    """
    Retrieve the latest 10 comments for a YouTube video.
    """
    try:
        # Get the service object
        service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        # Call the YouTube API to get the comments for the video
        comments_response = service.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=10
        ).execute()

        # Print the comments
        for item in comments_response["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            print(f"{author}: {text}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        comments_response = None

    return comments_response

if __name__ == "__main__":
    # Prompt the user for a YouTube video URL
    video_url = input("Enter the URL of a YouTube video: ")

    # Extract the video ID from the URL
    video_id = get_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL.")
    else:
        # Get and print the comments for the video
        get_video_comments(video_id)
