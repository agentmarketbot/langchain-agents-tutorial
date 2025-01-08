import keyboard
import os
import tempfile

import numpy as np
import openai
import sounddevice as sd
import soundfile as sf
import tweepy

from elevenlabs import generate, play, set_api_key
from langchain.agents import initialize_agent, load_tools
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from langchain.utilities.zapier import ZapierNLAWrapper


from dotenv import load_dotenv
load_dotenv()

elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
if not elevenlabs_api_key:
    raise ValueError("Please set ELEVENLABS_API_KEY environment variable")
set_api_key(elevenlabs_api_key)

openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

# Set recording parameters
duration = 5  # duration of each recording in seconds
fs = 44100  # sample rate
channels = 1  # number of channels


def record_audio(duration, fs, channels):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    print("Finished recording.")
    return recording


def transcribe_audio(recording, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        sf.write(temp_audio.name, recording, fs)
        temp_audio.close()
        with open(temp_audio.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        os.remove(temp_audio.name)
    return transcript["text"].strip()


def play_generated_audio(text, voice="Bella", model="eleven_monolingual_v1"):
    audio = generate(text=text, voice=voice, model=model)
    play(audio)


# Get Twitter API credentials from environment variables
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

if all([consumer_key, consumer_secret, access_token, access_token_secret]):
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
else:
    print("Warning: Twitter API credentials not fully configured. Twitter posting will not be available.")


class TweeterPostTool(BaseTool):
    name = "Twitter Post Tweet"
    description = "Use this tool to post a tweet to twitter."

    def _run(self, text: str) -> str:
        """Use the tool."""
        return client.create_tweet(text=text)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")


if __name__ == '__main__':

    llm = OpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")

    zapier_api_key = os.getenv('ZAPIER_NLA_API_KEY')
    if zapier_api_key:
        zapier = ZapierNLAWrapper(zapier_nla_api_key=zapier_api_key)
        toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
        tools = toolkit.get_tools()
    else:
        print("Warning: Zapier NLA API key not configured. Zapier integration will not be available.")
        tools = []

    # Add Twitter tool if credentials are configured
    if all([consumer_key, consumer_secret, access_token, access_token_secret]):
        tools.append(TweeterPostTool())

    # Always add human tools
    tools.extend(load_tools(["human"]))

    agent = initialize_agent(tools, llm, memory=memory, agent="conversational-react-description", verbose=True)

    while True:
        print("Press spacebar to start recording.")
        keyboard.wait("space")  # wait for spacebar to be pressed
        recorded_audio = record_audio(duration, fs, channels)
        message = transcribe_audio(recorded_audio, fs)
        print(f"You: {message}")
        assistant_message = agent.run(message)
        play_generated_audio(assistant_message)
