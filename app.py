import re
import requests
import os

# Try importing the required modules with error handling
try:
    from youtube_transcript_api import YouTubeTranscriptApi as yta
    print("Successfully imported youtube_transcript_api")
except ImportError as e:
    print(f"Error importing youtube_transcript_api: {e}")
    print("Please install it using: pip install youtube_transcript_api")
    exit(1)

try:
    from googleapiclient.discovery import build
    print("Successfully imported googleapiclient")
except ImportError as e:
    print(f"Error importing googleapiclient: {e}")
    print("Please install it using: pip install google-api-python-client")
    exit(1)

# For a single video
def get_single_video_transcript(video_id):
    try:
        data = yta.get_transcript(video_id)
        
        final_data = ''
        for val in data:
            for key, value in val.items():
                if key == 'text':
                    final_data += value + ' '
        
        process_data = final_data.splitlines()
        clean_data = ''.join(process_data)
        return clean_data
    except Exception as e:
        print(f"Error getting transcript for video {video_id}: {str(e)}")
        return ""

# For a playlist
def get_playlist_videos(playlist_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    videos = []
    next_page_token = None
    
    while True:
        playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        
        playlist_response = playlist_request.execute()
        
        for item in playlist_response['items']:
            video_id = item['contentDetails']['videoId']
            videos.append(video_id)
        
        next_page_token = playlist_response.get('nextPageToken')
        
        if not next_page_token:
            break
    
    return videos

# Function to save transcripts with word limit
def save_transcripts_with_limit(all_transcripts, max_words=500000):
    words = all_transcripts.split()
    total_words = len(words)
    
    if total_words <= max_words:
        # If under the limit, save to a single file
        with open("transcripts.txt", "w", encoding="utf-8") as f:
            f.write(all_transcripts)
        print(f"Transcripts saved to {os.path.abspath('transcripts.txt')} ({total_words} words)")
    else:
        # Split into multiple files
        file_count = 0
        start_idx = 0
        
        while start_idx < total_words:
            file_count += 1
            end_idx = min(start_idx + max_words, total_words)
            
            file_content = " ".join(words[start_idx:end_idx])
            filename = f"transcripts_part{file_count}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(file_content)
            
            print(f"Part {file_count} saved to {os.path.abspath(filename)} ({end_idx - start_idx} words)")
            start_idx = end_idx

# Main code
link = 'https://youtube.com/playlist?list=PLeHoly7hGE4XztXJh5hA9P_zneVclUxqR&si=WtCwmxSfk5_lKX0T'

# You need to get an API key from Google Cloud Console
API_KEY = "AIzaSyAllwhYA8Ws-5hu9-SJ5616h2MEPfPFrHY"  # Replace with your actual API key

# Extract playlist ID
playlist_id_match = re.search(r'list=([^&]+)', link)
if playlist_id_match:
    playlist_id = playlist_id_match.group(1)
    print(f"Processing playlist: {playlist_id}")
    
    try:
        video_ids = get_playlist_videos(playlist_id, API_KEY)
        
        if video_ids:
            all_transcripts = ""
            for i, video_id in enumerate(video_ids):
                print(f"Getting transcript for video {i+1}/{len(video_ids)}: {video_id}")
                transcript = get_single_video_transcript(video_id)
                
                if transcript:
                    all_transcripts += f"\n\n--- VIDEO {i+1} TRANSCRIPT ---\n\n"
                    all_transcripts += transcript
            
            print("\n\nSaving transcripts...")
            save_transcripts_with_limit(all_transcripts)
        else:
            print("No videos found in the playlist.")
    except Exception as e:
        print(f"Error processing playlist: {str(e)}")
else:
    # Handle single video case
    video_id_match = re.search(r'(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^?&]+)', link)
    if video_id_match:
        vid_id = video_id_match.group(1)
    else:
        # Alternative method if regex fails
        id_parts = link.split('/')
        vid_id = id_parts[-1].split('?')[0]
    
    transcript = get_single_video_transcript(vid_id)
    if transcript:
        save_transcripts_with_limit(transcript)
    else:
        print("No transcript available for this video.")