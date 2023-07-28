import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

# Grabbing the YouTube_API_KEY which is saved on my local computer beforehand
api_key = os.environ.get('YouTube_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

# Using regular expressions to search for these patters 
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0
nextPageToken = None

# This loop will go on until there is no next page left in the playlist 
while True:
    # Processing the YouTube API
    playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            # Let's look at one of the playlists of MrBeast Channel
            playlistId="PLoSWVnSA9vG9znrCdXo74jUKDqucZhA9-",
            maxResults=50,
            pageToken=nextPageToken,
        )

    playlist_response = playlist_request.execute()

    vid_ids = []
    for item in playlist_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        # Parsing the data found via the regular expressions 
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        # Checks if the playlist's videos are longer than hours and minutes, if not, assign them to 0
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        # Converting the duration represented in hours, minutes and seconds to seconds only
        video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()
        # Add up each video length in the playlist
        total_seconds += video_seconds

    # Going to the next page
    nextPageToken = playlist_response.get('nextPageToken')
    
    # If there is no next page, break out the while loop
    if not nextPageToken:
        break


# Convert the total duration of the playlist represenred in seconds to hours, minutes and seconds format
minutes, seconds = divmod(int(total_seconds), 60)
hours, minutes = divmod(minutes, 60)
print(f"{hours} hours {minutes} minutes and {seconds} seconds of content in this playlist")

youtube.close()


