import os

import anthropic
from dotenv import load_dotenv

load_dotenv(override=True)


class Claude():
    def __init__(self):
        self.client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.environ.get('ANTHROPIC_API_KEY'),
        )

    def summarise_video_transcript(self, video_transcript: str, model: str='haiku'):
        """
        Summarises a video transcript using Claude LLM
        Currently we use the haiku model, there is option to use a more powerful model - see comments
        """
        if model == 'haiku':
            model="claude-3-haiku-20240307"
        elif model == 'sonnet':
            model="claude-3-sonnet-20240229"
        elif model == 'opus':
            model="claude-3-opus-20240229"
        else:
            model="claude-3-haiku-20240307"

        message = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.0,
            system="""You are a expert educator, and summariser of information. 
            You summarise youtube video transcripts into short readable bites. 
            You give the appropriate amount of information to summarise a video, in short bullet points.
            You include all important information.
            You return a json object with the keys title and summary of bullet points like so:
            The title should be 2-4 words which are as descriptive as possible
            {
                "title": "LLM with Python",
                "summary": ["- Install python and pip",
                            "- install the requests library",
                            "- write a valid get request to query the completions API endpoint",
                            "- process the results"]
            }
            """,
            messages=[
                {"role": "user", "content": video_transcript},
                {'role': 'assistant', "content": '{'}
            ]
        )
        print(message)
        print(dir(message))
        print(f'Input tokens: {message.usage.input_tokens}')
        print(f'Output tokens: {message.usage.output_tokens}')
        # message.usage.output_tokens
        return message.content[0].text