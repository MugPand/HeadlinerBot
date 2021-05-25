# HeadlinerBot

HeadlinerBot is a discord bot that pings twitter accounts to keep servers up to date with breaking headlines. (Originally created to track sports news, however, is compatible with all public Twitter accounts!)

## Getting Started

To get started:

1. Create a .env file containing the following with your keys inputted:

    ```# .env
    # Discord Keys
    DISCORD_TOKEN=XXXXXX
    DISCORD_GUILD=XXXXXX
    SPORTS_CHANNEL=XXXXXX
    # Twitter Keys
    TWITTER_API_KEY=XXXXX
    TWITTER_API_SECRET_KEY=XXXXXX
    TWITTER_BEARER_TOKEN=XXXXXX
    TWITTER_ACCESS_TOKEN=XXXXXX
    TWITTER_ACCESS_TOKEN_SECRET=XXXXXX

1. Run ```pip install -r requirements.txt```
1. Start the bot by running ``` python bot.py ```

## Usage

The bot automatically scans Tweets every 5 minutes however, the number of tweets and various accounts that are being searched can be changed.

Commands available with the bot:

- ``` !accounts ``` displays a list of accounts that are being searched.
- ``` !addAccount 'account name' 'number of tweets' ``` allows the user to add a Twitter Account to be tracked by entering the Twitter username and number of tweets to be scanned in every 5 minute interval. *Number of tweets parameter is required to prevenet an overflow of tweets from accounts that are constantly posting.*
- ``` !deleteAccount 'account name' ``` deletes a Twitter Account from the internal accounts list.
- ``` !shutdown ``` shuts the bot down.
- ``` !help ``` displays a simple help menu similar to the content displayed in this section.

All internal functions and API requests are appropriately labeled and commented.
