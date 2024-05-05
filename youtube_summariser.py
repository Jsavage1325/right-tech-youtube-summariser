import json
import os
from time import sleep
from urllib.parse import parse_qs, urlparse

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from claude_llm import Claude


def get_video_id(url):
    """Extract video ID from YouTube URL."""
    query = urlparse(url).query
    video_id = parse_qs(query).get('v')
    if video_id:
        return video_id[0]
    return None

def get_video_title(url):
    yt = YouTube(url)
    return yt.title


def fetch_transcript(video_id):
    """Fetch the transcript of a video given its ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript)
        return text_transcript
    except Exception as e:
        print(f"Failed to fetch transcript for video {video_id}: {e}")
        return None

def summarise_video_transcript(transcript: str, title: str, model: str, prompt: str, api_key: str):
    """Summarize the video transcript."""
    if api_key:
        cl = Claude(api_key=api_key)
    else:
        cl = Claude()

    summary = cl.summarise_video_transcript(transcript, title, model, prompt)

    return summary

def clean_multiline_json(raw_json):
    """Preprocesses multiline and potentially malformed JSON strings to be JSON-compliant."""
    try:
        # Attempt to directly load the JSON to check if it's already valid
        return json.loads(raw_json)
    except json.JSONDecodeError:
        # If it fails, preprocess and try again
        cleaned_lines = []
        for line in raw_json.splitlines():
            # Escape double quotes and wrap lines in double quotes if not already
            cleaned_line = line.replace('"', '\\"').strip()
            if not cleaned_line.startswith('"'):
                cleaned_line = '"' + cleaned_line + '"'
            cleaned_lines.append(cleaned_line)
        cleaned_json = "[" + ",\n".join(cleaned_lines) + "]"
        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON after cleaning:", e)
            return None

def save_summary(summary, video_name, path: str=None):
    """Save the summary text into a file, appending a suffix if the file exists."""
    if path:
        os.makedirs(path, exist_ok=True)
    else:
        os.makedirs('summaries', exist_ok=True)
    counter = 0
    while True:
        suffix = f"-{counter}" if counter > 0 else ""
        if path: 
            file_path = os.path.join(path, f'{video_name}{suffix}.txt')
        else:
            file_path = os.path.join('summaries', f'{video_name}{suffix}.txt')
        
        if not os.path.exists(file_path):
            break
        counter += 1
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(summary)

def save_transcript(transcript, video_name):
    """Save the transcript text into a file, appending a suffix if the file exists."""
    os.makedirs('transcripts', exist_ok=True)
    counter = 0
    while True:
        suffix = f"-{counter}" if counter > 0 else ""
        file_path = os.path.join('transcripts', f'{video_name}{suffix}.txt')
        if not os.path.exists(file_path):
            break
        counter += 1
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(transcript)

def main(video_urls, prompt, model: str, api_key: str=None):
    """Process each video URL provided and return results as a dictionary."""
    results = {}
    for url in video_urls:
        try:
            video_id = get_video_id(url)
            if video_id:
                transcript = fetch_transcript(video_id)
                title = get_video_title(url)
                if transcript:
                    # Generate summary
                    summary = summarise_video_transcript(transcript, title, model, prompt, api_key)
                    summary_filename = f"{title.replace(' ', '-')}-summary.txt"
                    results[summary_filename] = summary.encode('utf-8')  # Encode summary as bytes

                    sleep(15)  # Throttle requests to avoid overloading servers or hitting API limits
                else:
                    print(f"Could not fetch transcript for video {video_id}.")
            else:
                print("Invalid YouTube URL:", url)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            print(f'Error processing: {url}.')
    return results

# def main(video_urls, prompt, should_save_transcript: bool, model: str, output_path: str=None, api_key: str=None):
#     """Process each video URL provided."""

#     for url in video_urls:
#         try:
#             video_id = get_video_id(url)
#             if video_id:
#                 transcript = fetch_transcript(video_id)
#                 title = get_video_title(url)
#                 if transcript:
#                     summary = summarise_video_transcript(transcript, title, model, prompt, api_key)
#                     save_summary(summary, title.replace(' ', '-'), output_path)
#                     if should_save_transcript:
#                         save_transcript(transcript, title.replace(' ', '-'))
#                     sleep(15)
#                 else:
#                     print(f"Could not fetch transcript for video {video_id}.")
#             else:
#                 print("Invalid YouTube URL:", url)
#         except KeyboardInterrupt:
#             exit()
#         except Exception as e:
#             print(e)
#             print(f'Error processing: {url}.')

# if __name__ == "__main__":
#     # Input files
#     with open('youtube_urls.txt', 'r') as f:
#         video_urls = f.readlines()

#     main(video_urls, should_save_transcript=False, model='haiku')
