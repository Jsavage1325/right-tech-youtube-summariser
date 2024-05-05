import json
import zipfile
from io import BytesIO
import requests

import streamlit as st

from youtube_summariser import main

# Constants
API_KEY = '$2a$10$eQCkEq9KGPXNfF1sSV1T1.d0FCZCLg/Fsbx4pGKZShiJPsCW29Voy'  # Use your actual API key here
BIN_ID = '6637e954acd3cb34a8436bc8'  # Use your actual bin ID here
API_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"

headers = {
    "Content-Type": "application/json",
    "X-Access-Key": API_KEY
}

def fetch_data():
    response = requests.get(f"{API_URL}/latest", headers=headers)
    print(response.text)
    if response.status_code == 200:
        data = response.json()['record']
        return data['prompt'], data['urls']
    else:
        st.error("Failed to fetch data from JSONBin.io")
        return "", ""  # Default empty prompt and URLs

def save_data(prompt, urls):
    data = {
        "prompt": prompt,
        "urls": urls
    }
    response = requests.put(API_URL, headers=headers, json=data)
    if not response.ok:
        st.error("Failed to save data to JSONBin.io")

def run_script(video_urls, model, prompt, api_key):
    """
    Runs the main script of YouTube Summariser, this returns a dictionary containing the required values
    """
    return main(video_urls, prompt, False, model, None, api_key)

def start_processing(video_urls, model, prompt, api_key):
    results = run_script(video_urls, model, prompt, api_key)
    # Create ZIP file in memory for all the output files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, filedata in results.items():
            zip_file.writestr(filename, filedata)
    return zip_buffer

# Initialize Streamlit layout
st.title("YouTube Video Summarizer")
default_prompt, default_urls = fetch_data()
video_urls = st.text_area("Enter Video URLs, one per line:", value=default_urls)
model = st.selectbox("Choose Model:", ["haiku", "sonnet", "opus"])
prompt = st.text_area("Enter Prompt:", value=default_prompt)
api_key = st.text_input("Enter API Key:", type="password")

if st.button("Save Changes"):
    save_data(prompt, video_urls)
    st.success("Changes saved successfully!")

if st.button("Start Processing"):
    if not video_urls.strip():
        st.warning("Please enter at least one video URL.")
    elif not api_key.strip():
        st.warning("Please enter your API Key.")
    else:
        video_url_list = video_urls.split()
        zip_buffer = start_processing(video_url_list, model, prompt, api_key)
        st.success("Processing complete! Downloading results...")
        # Download the ZIP file
        st.download_button(
            label="Download Results",
            data=zip_buffer.getvalue(),
            file_name="summarized_videos.zip",
            mime="application/zip"
        )

st.button("Quit", on_click=st.stop)
