import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from googleapiclient.discovery import build
from IPython.display import JSON    

api_key = "AIzaSyAE_OqRS9NzqQLhC37Lf8nxxUppbpBuufw"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)



channel_names_input = input("Enter the YouTube channel names separated by commas: ")
channel_names =  [name.strip() for name in channel_names_input.split(",")]
channel_ids = []

for channel_name in channel_names:
    request = youtube.channels().list(
        part = "snippet",
        forUsername=channel_name
    )
    response = request.execute()

    if response["items"]:
        channel_id = response["items"][0]["id"]
        print(f"Channel ID for {channel_name}: {channel_id}")
        channel_ids.append(channel_id)
    else:
        print(f"Channel '{channel_name}' not found")


JSON(response)

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=",".join(channel_ids),
)
    
response = request.execute()

for item in response ['items']:
    data = {'channelNName': item["snippet"]["title"],
            'subscribers': item['statistics']['subscriberCount'],
            'views': item['statistics']['viewCount'],
            'totalViews': item['statistics']['videoCount'],
            'playlistId':item['contentDetails']['relatedPlaylists']['uploads']

            
            
            }




    
