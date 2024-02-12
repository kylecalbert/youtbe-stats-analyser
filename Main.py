import googleapiclient.discovery
import pandas as pd 
from api_keys import YOUTUBE_API_KEY

def build_youtube_service(api_key):
    """
    Builds and returns a YouTube API service object.
    """
    api_service_name = "youtube"
    api_version = "v3"
    return googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

def get_playlist_ids(youtube, channel_names):
    """
    Retrieves the playlist IDs associated with the specified YouTube channels.
    """
    playlist_ids = {}
    for channel_name in channel_names:
        request = youtube.channels().list(
            part="contentDetails",
            forUsername=channel_name
        )
        response = request.execute()
        if response['items']:
            playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            playlist_ids[channel_name] = playlist_id
        else:
            print(f"Channel '{channel_name}' not found")
    return playlist_ids

def get_video_ids(youtube, playlist_ids):
    """
    Retrieves the video IDs from the playlists associated with the specified channel IDs.
    """
    video_ids = {}
    for channel_name, playlist_id in playlist_ids.items():
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        video_ids[channel_name] = [item['contentDetails']['videoId'] for item in response.get('items', [])]
    return video_ids

def get_video_stats(youtube, video_ids):
    """
    Retrieves statistics for the specified video IDs.
    """
    video_info = []
    for channel_name, ids in video_ids.items():
        for video_id in ids[:5]:
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            if response['items']:
                video_data = response['items'][0]
                title = video_data['snippet'].get('title', 'Unknown')
                views = video_data['statistics'].get('viewCount', 0)
                likes = video_data['statistics'].get('likeCount', 0)
                dislikes = video_data['statistics'].get('dislikeCount', 0)
                comments = video_data['statistics'].get('commentCount', 0)
                tags = video_data['snippet'].get('tags', [])
                published = video_data['snippet'].get('publishedAt', 'Unknown')
                duration = video_data['contentDetails'].get('duration', 'Unknown')
                video_info.append({
                    "Channel": channel_name,
                    "Title": title,
                    "Views": views,
                    "Likes": likes,
                    "Dislikes": dislikes,
                    "Comments": comments,
                    "Tags": tags,
                    "Duration": duration,
                    "Publish Date": published
                })
            else:
                print(f"Video with ID {video_id} not found")
    return pd.DataFrame(video_info)

def get_channel_ids(youtube, channel_names):
    """
    Retrieves the channel IDs associated with the specified channel names.
    """
    channel_ids = {}
    for channel_name in channel_names:
        request = youtube.channels().list(
            part="contentDetails",
            forUsername=channel_name
        )
        response = request.execute()
        if response['items']:
            channel_id = response['items'][0]['id']
            channel_ids[channel_name] = channel_id
        else:
            print(f"Channel '{channel_name}' not found")
    return channel_ids

def get_channel_stats(youtube, channel_ids):
    """
    Retrieves statistics for the specified channel IDs.
    """
    channel_data = []
    for channel_name, channel_id in channel_ids.items(): 
        request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        )
        response = request.execute()
        for item in response.get('items', []):
            stats = item.get('statistics', {})
            channel_data.append({
                "Channel": item['snippet']['title'],
                "Subscribers": stats.get('subscriberCount', 0),
                "Views": stats.get('viewCount', 0),
                "Videos": stats.get('videoCount', 0)
            })
    return pd.DataFrame(channel_data)

def main():
    youtube = build_youtube_service(YOUTUBE_API_KEY)
    channel_names_input = input("Enter the YouTube channel names separated by commas: ")
    channel_names = [name.strip() for name in channel_names_input.split(",")]

    playlist_ids = get_playlist_ids(youtube, channel_names)
    video_ids = get_video_ids(youtube, playlist_ids)
    video_df = get_video_stats(youtube, video_ids)
    channel_ids = get_channel_ids(youtube, channel_names)
    channel_df = get_channel_stats(youtube, channel_ids)

    print("Video Data:")
    print(video_df)
    print("\nChannel Data:")
    print(channel_df)

if __name__ == "__main__":

    main()
