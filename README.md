# YouTube Video Summariser
- Takes a list of YouTube video urls as in `youtube_urls.txt`
- For each URL
  - Extract the video ID
  - Use the video ID to get the transcript using the YouTube transcript API
  - Pass the transcript to the Anthropic model to generate a title and summary
  - Saves the summary in a file with the title as a name, and the bullet point summary inside in /summaries
  - If should_save_transcript = True also saves the transcript in a file with the suggested name in /transcripts
  - Sleeps for 15 seconds to avoid issues with the Anthropic API rate limits

Use CTRL-C (windows) or COMMAND-C (Mac) to exit the script.
Error handling is in place, errors are handled gracefully, and you will see the errors in the console.

## Setup
Ensure Python is installed and 

Install dependencies
`pip install -r requirements.txt`

Create a `.env` file with an Anthropic API key as so
`ANTHROPIC_API_KEY=sk-ant-api03-g-...XYZ`

Update the required URLs in `youtube_urls.txt`

Optionally change the model or set transcript saving by changing args here
`main(video_urls, should_save_transcript=False, model='haiku')`
Supported models are `haiku`, `sonnet` and `opus`.

## Running
Please run the code using the following
`/path/to/.venv/bin/python /path/to/youtube_summariser.py`

## Limitations
The main limitation in this script is the 15 second sleep we have to avoid the rate limitations for the 'free' plan.
If you have a more advanced plan with Anthropic, the sleep can be reduced.
The first paid tier increases the rate limiting to 50 RPM (requests per minute), which would allow for 10x faster requests.

The other thing to consider is the tokens per day, as we are throwing a lot of tokens at the model, we may reach these limits. Please see [here](https://docs.anthropic.com/claude/reference/rate-limits) for more details.