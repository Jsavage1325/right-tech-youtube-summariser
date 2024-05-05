import os

import anthropic
from dotenv import load_dotenv

load_dotenv(override=True)


class Claude():
    def __init__(self, api_key: str=None):
        self.client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=api_key if api_key else os.environ.get('ANTHROPIC_API_KEY'),
        )

    def summarise_video_transcript(self, video_transcript: str, title: str, model: str='haiku', prompt: str=None):
        """
        Summarises a video transcript using Claude LLM
        Currently we use the haiku model, there is option to use a more powerful model - see comments
        """
        if prompt == None:
            prompt = """
            You are a expert educator, and summariser of information. 
            Summarise the following with 6-10 bullet points plus 2-3 sentences amplifying comments.  When finished, note any recommended action items. 
            Please tell me only the summary.
            """
        print('Using prompt: ', prompt)
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
            max_tokens=4000,
            temperature=0.0,
            system=prompt,
            messages=[
                {"role": "user", "content": f"Title: \n{title}\nTranscript:\n{video_transcript}"},
            ]
        )
        print(message)
        print(f'Input tokens: {message.usage.input_tokens}')
        print(f'Output tokens: {message.usage.output_tokens}')
        # message.usage.output_tokens
        return message.content[0].text

    def summarise_video_transcript_old(self, video_transcript: str, model: str='haiku'):
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
            max_tokens=4000,
            temperature=0.0,
            system="""You are a expert educator, and summariser of information. 
            You summarise youtube video transcripts into short readable bites. 
            You will return 6-10 summary bullet points as a json list which are 2-3 sentences long.
            You will return any actions items suggested by the video as a json list. If there are none, return an empty array.
            You include all important information.
            You return a json object with the keys title, summary and action_items of bullet points like so:
            The title should be as few words as possible that are as descriptive as possible
            {
                "title": "New Electric Car Tax Rules",
                "summary": ["U.S. Goverment has reduced taxes for electric vehicles to a negative amount. This affects all electric vehicles in U.S., but Tesla as the largest manufacturer has been impacted the most.",
                            "The push for electric cars has reached a point never seen before, as pollutants in the atmosphere reach an all time high. The temperatures have risen over 1.5 degrees in the past 24 months.",
                            "The U.S. govemernment has also put 7 quadrillion dollars of funding into renewables. The only thing the people are asking is, is it too little too late?",
                            "This means serious news for investors, green energy is the highest increasing investment value, reaching a 10000% green energy market cap increase in 48 hours. Warren Buffet who was shorting these markets has gone bankrupt. This news is unprecedented, and an entirely entirely new chapter in human history, if not the last."]
                "action_items": ["Go invest in Tesla now",
                            "Invest in the electric car market"]
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

    def apply_for_freelance_gig(self, job_description: str):
        """
        Summarises a video transcript using Claude LLM
        Currently we use the haiku model, there is option to use a more powerful model - see comments
        """
        # if model == 'haiku':
        #     model="claude-3-haiku-20240307"
        # elif model == 'sonnet':
        #     model="claude-3-sonnet-20240229"
        # elif model == 'opus':
        model="claude-3-opus-20240229"
        # else:
        #     model="claude-3-haiku-20240307"

        message = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.0,
            system="""You are a technical expert, and freelancer on the platform UpWork. 
            You are an expert at applying for roles, you create a brief plan or description of how you can 
            do the work.
            You highlight your motivations for the role.
            You have a first class computer science degree.
            You have 5 years of experience in working with various technologies, focusing on:
            - backend development
            - devops
            - cloud infrastructure
            - Data Engineering (SQL, DBT, Data warehousing, databases)
            - application security engineering
            - frontend development
            - Large Language models
                - Claude
                - OpenAI
                - Langchain
                - Instructor LLM
                - Midjourney
                - Whisper transcription models
            - AI/ML
                - LLM powered tool to scrape contact data using a list of websites, gathers and genrates 20k cold emails per day
                - LLM powered tool to generate dynamic questions for a DuoLingo style education app using spaced repetitive learning
                - LLM powered app which cleans excel data which is generated from third party software - allows for cleaning of data not possible unless manually done pre-LLM
                - LLM powered app to allow for CV to job matching using semantic scoring. Also provides summaries and suggested improvements. Uses knowledge of CV structure processed by ATS

            """,
            messages=[
                {"role": "user", "content": job_description}
            ]
        )
        # print(message)
        # print(dir(message))
        # print(f'Input tokens: {message.usage.input_tokens}')
        # print(f'Output tokens: {message.usage.output_tokens}')
        # message.usage.output_tokens
        return message.content[0].text

# cl = Claude()
# gig_details = """
# Export in LLM and AI like ChatGPT to help us use these technologies based on our company knowledge
# Posted 3 hours ago
# Only freelancers located in the U.K. may apply.
# We are looking for somebody to help us utilise a LLM like ChatGPT based on the information inside our extensive knowledge base.

# We are looking for somebody with a previous experience working on such projects and who understands how to develop an integration to allow our ever changing kb to be queried via natural language.  We need to understand the costs, benefits and any security considerations of using such systems.

# If we find the right person this role might extend into how we can use AI to analyse other parts of our data landscape.
# """
# application = cl.apply_for_freelance_gig(gig_details)
# print(application)