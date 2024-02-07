import googleapiclient.discovery

api_key = "AIzaSyAE_OqRS9NzqQLhC37Lf8nxxUppbpBuufw"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key
)

def get_playlist_ids(youtube, channel_names):
    playlist_ids = {}
    for channel_name in channel_names:
        request = youtube.channels().list(
            part="contentDetails",
            forUsername=channel_name
        )
        response = request.execute()
        if response['items']:
            playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            playlist_ids[channel_name] = playlist_id #looping through each channel and sotring the channel name with playlust id as pair ie: "ufc:"Zshsxn2351vsa""
        else:
            print(f"Channel '{channel_name}' not found")
    return playlist_ids
    
all_video_ids = {}
def get_video_ids(youtube, playlist_ids):
    for channel_name, playlist_id in playlist_ids.items(): #looping through the channel name and playlist id to gtet the values of both
        video_ids = []
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        all_video_ids[channel_name] = video_ids #channel name will then get stored alongside the video id as pair 
    # print(all_video_ids)
    return all_video_ids

def get_video_stats(youtube, all_video_ids):
    for channel_name, video_ids in all_video_ids.items(): # Loop through each channel and its video IDs
        print(f"Video Stats for {channel_name}:")
        for video_id in video_ids[:5]: # Loop through the first 5 video IDs
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            if response['items']:
                video_data = response['items'][0]
                title = video_data['snippet']['title']
                views = video_data['statistics']['viewCount']
                likes = video_data['statistics'].get('likeCount', 0)
                dislikes = video_data['statistics'].get('dislikeCount', 0)
                print(f"Title: {title}")
                print(f"Views: {views}")
                print(f"Likes: {likes}")
                print(f"Dislikes: {dislikes}")
                print()
            else:
                print(f"Video with ID {video_id} not found")

def main():
    channel_names_input = input("Enter the YouTube channel names separated by commas: ")
    channel_names = [name.strip() for name in channel_names_input.split(",")]

    playlist_ids = get_playlist_ids(youtube, channel_names)

    all_video_ids = get_video_ids(youtube, playlist_ids)

    get_video_stats(youtube, all_video_ids)
    # print("Video IDs:")
    # for channel_name, ids in video_ids.items():
    #     print(f"{channel_name}: {', '.join(ids)}")

if __name__ == "__main__":
    main()
