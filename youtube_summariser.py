import json
import os
from time import sleep
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from claude_llm import Claude

cl = Claude()

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    query = urlparse(url).query
    video_id = parse_qs(query).get('v')
    if video_id:
        return video_id[0]
    return None

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

def summarise_video_transcript(transcript: str, model: str):
    """Summarize the video transcript."""
    incomplete_json_object = cl.summarise_video_transcript(transcript, model)

    result_object = json.loads('{' + incomplete_json_object)

    return result_object.get('title'), '\n'.join(result_object.get('summary'))

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

def save_summary(summary, video_name):
    """Save the summary text into a file, appending a suffix if the file exists."""
    os.makedirs('summaries', exist_ok=True)
    counter = 0
    while True:
        suffix = f"-{counter}" if counter > 0 else ""
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

def main(video_urls, should_save_transcript: bool, model: str):
    """Process each video URL provided."""
    for url in video_urls:
        try:
            video_id = get_video_id(url)
            if video_id:
                transcript = fetch_transcript(video_id)
                if transcript:
                    title, summary = summarise_video_transcript(transcript, model)

                    save_summary(summary, title.replace(' ', '-'))
                    if should_save_transcript:
                        save_transcript(transcript, title.replace(' ', '-'))
                    sleep(15)
                else:
                    print(f"Could not fetch transcript for video {video_id}.")
            else:
                print("Invalid YouTube URL:", url)
        except KeyboardInterrupt:
            exit()
        except:
            print(f'Error processing: {url}.')

if __name__ == "__main__":
    # Input files
    with open('youtube_urls.txt', 'r') as f:
        video_urls = f.readlines()

    main(video_urls, should_save_transcript=False, model='haiku')
