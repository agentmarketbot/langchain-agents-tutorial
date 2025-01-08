<!-- @format -->

# Virtual Assistant with Langchain

This is a basic guide on how to set up and run a virtual assistant project that connects to your calendar, email, and Twitter accounts using Langchain, Tweepy, and Zapier.

[![Youtube thumbnail](thumb.png)](https://youtu.be/N4k459Zw2PU)

## Prerequisites

1. Python 3.6 or higher
2. `tweepy` library
3. `langchain` library

To install the required libraries, run:

```bash
pip install -r requirements.txt
```

## Setting up API keys

You need to obtain API keys for the following services:

1. Twitter Developer Account (for Tweepy)
2. OpenAI API key
3. Zapier NLA API key
4. ElevenLabs API key

Copy the `.env.example` file to `.env` and fill in your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
TWITTER_CONSUMER_KEY=your_twitter_consumer_key_here
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here
ZAPIER_NLA_API_KEY=your_zapier_api_key_here
```

Replace `your_*_api_key_here` with your actual API keys.

**Important**: 
1. Never commit your API keys to version control. The `.env` file is already in `.gitignore` to prevent accidental commits.
2. If you see an error like "Did not find openai_api_key", it means your environment variables are not properly set. Make sure you've created the `.env` file and filled in all the required API keys.

## Running the program

1. Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```
2. Open a terminal or command prompt and navigate to the folder containing `main.py`.
3. Run the program using the following command:

```bash
python main.py
```

4. The program will start an interactive session where you can type your messages to the virtual assistant. The assistant will respond to your queries based on the available tools and integrations.

## Example usage

You can interact with the virtual assistant using natural language, as it is capable of understanding and executing actions based on your input.

Examples:

- "Post a tweet saying 'Hello, World!'"
- "Schedule a meeting tomorrow at 3 PM"
- "Send an email to john@example.com with the subject 'Meeting reminder' and the message 'Don't forget our meeting tomorrow at 3 PM.'"

To exit the program, press `Ctrl+C` or close the terminal window.
