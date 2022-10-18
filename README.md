# Midgard Calendar Discord Bot

I love playing D & D and have a fair number of online D & D groups. I help run a westmarches game in the Midgard setting and have been for almost 6 months. After day in day out of hand typing up a Discord post about what the ingame day was I got fed up. Over the course of a week I coded a Discord bot that would post for me, no more forgetting to post! 

While this is niche to my game, it could be a great easy jumping off point for someone else to make their own Discord bot to post to their home game. No need to spend money every month to get a bot to post to your game when you could do it for free. I'm sure other people have done something similar, but this was a great personal project and a fun way to delve deeper into what a Discord bot can really do.

## Key Parts of the Bot

Using a JSON file from our previous online calendar we are able to keep track of the current ingame date, move through the different events, and use predetermined calendar information like days of the week and how many days are in a month. Most of the work this bot does is using and manipulating information from this JSON file.

<img src="https://github.com/MarnieRM/Midgard-Calander/blob/main/ReadmeImages/JSON.PNG" width=50% height=50%>

There are a variety of functions in the code that helps us generate the date information for a discord post that is sent once every 24 hours using the looping functionality of tasks. This getCalander() function orchestrates everything in the program.

<img src="https://github.com/MarnieRM/Midgard-Calander/blob/main/ReadmeImages/loopFunction.PNG" width = 75% height = 75%>

At the end of the getCalander() function is a variety of updates to the JSON. These move the day ahead by 3 (the amount of ingame days per irl day) in preparation for the post the next day. Because we are editing the JSON directly there is a backup JSON file in case anything were to happen to foobar the original JSON file.

<img src="https://github.com/MarnieRM/Midgard-Calander/blob/main/ReadmeImages/update.PNG" width = 75% height = 75%>

## What Does a Post Look Like?

In line with the original posts on our discord, the similar style should help ensure a smooth transition from me to a bot for our users.

<img src="https://github.com/MarnieRM/Midgard-Calander/blob/main/ReadmeImages/Post.PNG" width = 75% height = 75%>

## What I Would Like to Add?

- Code to handle what to do if the bot goes down.
- Code to let me easily upload the bot to a Raspberry Pi for hosting.
- Add the Birch Queen Fair to the JSON events

## Libraries

[discord.py](https://github.com/Rapptz/discord.py)


## License

[MIT](https://github.com/MarnieRM/Midgard-Calander/blob/main/LISCENSE.txt)
