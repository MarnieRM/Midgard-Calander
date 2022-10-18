from discord.ext import tasks, commands
import discord
import os
from dotenv import load_dotenv
import json
import re
import asyncio

"""
Set up a .env file for the discord token
There are 3 JSON files in this project:
One is the original JSON file (test.json)
One is a backup of the edited JSON file (backup.json)
One is the current working JSON (newtest.json)
"""

#General setup for a discord bot
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
client = discord.Client(command_prefix=".", intents=intents)

#Setting up a regular expression for removing html from text. Could be removed if I change the json files in the future
REGCLEAN = re.compile('<.*?>')

#loads in the working json file
with open('newtest.json') as f:
    data = json.load(f)


def calculateMoon(currentLunar):
    """
    Translates the lunar day into a lunar phase
    :param currentLunar: The a lunar date from the 30.5 day cycle
    :return: The current lunar phase given the a lunar date
    """
    totalDays = 366
    lunarCycle = 30.5
    lunarDay = 30.5 / 24
    lunarPhase = ["New Moon", "New Moon Fading", "Waxing Crescent Rising", "Waxing Crescent", "Waxing Crescent Fading", "First Quarter Rising", "First Quarter", "First Quarter Fading", "Waxing Gibbous Rising", "Waxing Gibbous", "Waxing Gibbous Fading", "Full Moon Rising", "Full Moon", "Full Moon Fading", "Waning Gibbous Rising", "Waning Gibbous",
                  "Waning Gibbous Fading", "Third Quarter Rising", "Third Quarter", "Third Quarter Fading", "Waning Crescent Rising", "Waning Crescent", "Waning Crescent Fading", "New Moon Rising"]

    return lunarPhase[int((currentLunar / lunarDay) +0.2)]

def calculateFullMoon(currentLunar):
    """
    Given a lunar day, returns how many lunar days until the next full moon
    :param currentLunar: The a lunar date from the 30.5 day cycle
    :return: Returns the days until the next full moon
    """
    fullOn = 15.25
    if currentLunar > fullOn:
        daysUntil = abs(fullOn+30.5 - currentLunar)
    else:
        daysUntil = abs(fullOn - currentLunar)
    return daysUntil


def getDayWithEnd(day):
    """
    Adds an ending to a given day and turns it into a string
    :param day: A numeric day
    :return: A day as a string with an ending (e.g. 1st)
    """
    if (day > 3 and day < 21) or (day > 33) or (day > 23 and day < 31):
        writtenDay = str(day) + "th"
    elif (day == 3) or (day == 23):
        writtenDay = str(day) + "rd"
    elif (day == 2) or (day == 22) or (day == 32):
        writtenDay = str(day) + "nd"
    else:
        writtenDay = str(day) + "st"
    return writtenDay


def eventGrabber():
    """
    Gets all the events from the JSON
    :return: A list of all the events as strings ready to be printed
    """
    listOfEvents = []
    eventPost = ""
    for event in data["events"]:
        if event["data"]["conditions"]["Month"] == data["dynamic_data"]["timespan"] or event["data"]["conditions"][
            "Month"] == int(data["dynamic_data"]["timespan"]) + 1:
            #If the event is in this month or the next month

            if event["data"]["conditions"]["Month"] == int(data["dynamic_data"]["timespan"]) + 1 and int(
                    (event["data"]["conditions"]["Day"] <= (((data["dynamic_data"]["day"] + 14)) % int(data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"])) < ((data["dynamic_data"]["day"] + 14)))):
                #If the event is next month *and* the event day is less than or equal to what the day would be in two weeks(next month) (which should be less than the date in two weeks given it isnt next month)
                writtenDay = getDayWithEnd(event["data"]["conditions"]["Day"])

                if event["data"]["duration"] !=0:
                    #if that event is longer than a single day next month
                    endDay = getDayWithEnd(event["data"]["conditions"]["Day"] + event["data"]["duration"])
                    listOfEvents.append("-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                                        data["static_data"]["year_data"]["timespans"][
                                            event["data"]["conditions"]["Month"]][
                                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")

                else:
                    #if the event is just a single day next month
                    listOfEvents.append("-The " + event["name"] + " on the " + writtenDay + " of " +
                                        data["static_data"]["year_data"]["timespans"][event["data"]["conditions"]["Month"]][
                                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")


            elif event["data"]["conditions"]["Day"] > data["dynamic_data"]["day"] and (event["data"]["conditions"]["Day"] <= data["dynamic_data"]["day"] + 14) and event["data"]["conditions"]["Month"] == int(data["dynamic_data"]["timespan"]):
                writtenDay = getDayWithEnd(event["data"]["conditions"]["Day"])
                #if the event is in the future (greater than the current day) *and* the day of the event is less than two weeks from the current day *and* it is this month

                if event["data"]["duration"] !=0:
                    #if the event is longer than a single day this month

                    endDay = getDayWithEnd(event["data"]["conditions"]["Day"] + event["data"]["duration"])
                    listOfEvents.append(
                        "-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                        data["static_data"]["year_data"]["timespans"][
                            event["data"]["conditions"]["Month"]][
                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")

                else:
                    #if the event is just a single day this month
                    listOfEvents.append("-The " + event["name"] + " on the " + writtenDay + " of " +
                                        data["static_data"]["year_data"]["timespans"][
                                            event["data"]["conditions"]["Month"]]["name"] + "\n" + REGCLEAN.sub('',
                                                                                                                event[
                                                                                                                    "description"]) + "\n\n\n")
            elif (event["data"]["duration"] > 0):
                    #if the event is longer than a single day
                if (event["data"]["conditions"]["Day"] + event["data"]["duration"]) > data["dynamic_data"]["day"] and (
                        (event["data"]["conditions"]["Day"] +event["data"]["duration"]) <= data["dynamic_data"]["day"] + 14) and \
                        event["data"]["conditions"]["Month"] == int(data["dynamic_data"]["timespan"]):
                    #if the event start day plus its durration is greater than the current day *and* the start day plus the durration is less than or equal to two weeks in the future *and* it is this month
                    writtenDay = getDayWithEnd(event["data"]["conditions"]["Day"])

                    endDay = getDayWithEnd(event["data"]["conditions"]["Day"] + event["data"]["duration"])
                    listOfEvents.append(
                        "-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                        data["static_data"]["year_data"]["timespans"][
                            event["data"]["conditions"]["Month"]][
                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")

                if event["data"]["conditions"]["Month"] == int(data["dynamic_data"]["timespan"]) + 1 and int(
                        ((event["data"]["conditions"]["Day"] + event["data"]["duration"]) <= (((data["dynamic_data"]["day"] + 14)) % int(
                            data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]][
                                "length"])) < ((data["dynamic_data"]["day"] + 14)))):
                    #If the event is next month *and* the start day plus the durration of the event is less than two weeks from now in the next month (which should be less than two weeks from now assuming it is not next month)
                    writtenDay = getDayWithEnd(event["data"]["conditions"]["Day"])

                    endDay = getDayWithEnd(event["data"]["conditions"]["Day"] + event["data"]["duration"])
                    listOfEvents.append(
                        "-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                        data["static_data"]["year_data"]["timespans"][
                            event["data"]["conditions"]["Month"]][
                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")

            if event["data"]["conditions"]["week"] == 4:
                #if the event starts on the fourth week
                if ((((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7 ) + 15) == 15 and data["dynamic_data"]["day"] <= (
                        ((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7) + 21  +event["data"][
                            "duration"])):
                    #if the event day minus the day of the week mod 7 plus 15 (aka, the start of the 3rd week), comes out to 15, *and* the current day is less than the true start of the 3rd week( given the previous clause turns out to be 15) plus the durration
                    writtenDay = getDayWithEnd(
                        ((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7) + 21)

                    endDay = getDayWithEnd(
                        ((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7) + 21  +event["data"][
                            "duration"])
                    listOfEvents.append(
                        "-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                        data["static_data"]["year_data"]["timespans"][
                            event["data"]["conditions"]["Month"]][
                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")
                elif (data["dynamic_data"]["day"] <= (
                        ((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7) + 15  +event["data"][
                            "duration"])):
                    #if the current day is less than the start of the 3rd week (given in the fashion of the previous comment)
                    writtenDay = getDayWithEnd(((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7 ) + 15)

                    endDay = getDayWithEnd(((data["dynamic_data"]["day"] - data["dynamic_data"]["day_of_week"]) % 7 ) + 15  + event["data"]["duration"])
                    listOfEvents.append(
                        "-The " + event["name"] + " on the " + writtenDay + " until the " + endDay + " of " +
                        data["static_data"]["year_data"]["timespans"][
                            event["data"]["conditions"]["Month"]][
                            "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")

        elif (data["dynamic_data"]["timespan"]+1 > 11 and event["data"]["conditions"]["Month"] == 0 and (event["data"]["conditions"]["Day"] <= (((data["dynamic_data"]["day"] + 14)) % int(data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"])) < ((data["dynamic_data"]["day"] + 14)))):
            #if this is the 12th month *and* the event is in the first month and the event is within two weeks of the current day
            writtenDay = getDayWithEnd(event["data"]["conditions"]["Day"])

            listOfEvents.append("-The " + event["name"] + " on the " + writtenDay + " of " +
                                data["static_data"]["year_data"]["timespans"][event["data"]["conditions"]["Month"]][
                                    "name"] + "\n" + REGCLEAN.sub('', event["description"]) + "\n\n\n")






    return listOfEvents


def futureDateMonth(daysAhead):
    """
    Gets the future date information given an ammount of time in the future
    :param daysAhead: number of days from the current day
    :return: a string detailing a day, "daysAhead" number in the future
    """
    currentDate = int(data["dynamic_data"]["day"]) + int(daysAhead)
    currentMonthSize = data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"]
    newDate = currentDate % currentMonthSize
    writtenDay = getDayWithEnd(newDate)

    if newDate < currentDate:
        if data["dynamic_data"]["timespan"] + 1 < 12:
            return writtenDay + " of " + \
                   data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"] + 1]["name"]
        else:
            return writtenDay + " of " + \
                   data["static_data"]["year_data"]["timespans"][0]["name"]
    return writtenDay + " of " + data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["name"]




@tasks.loop(seconds = 24)
async def getcalender():
    """
    Every 24 hours, print all the day of the week information and move the clock forward 3 days
    """
    message_channel = client.get_channel(1030054713305088010) #gets channel information (change for different servers)
    #gets all the relevent information
    currentDate = data["static_data"]["year_data"]["global_week"][data["dynamic_data"]["day_of_week"]]
    currentMonth = data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["name"]
    events = eventGrabber()
    writtenDay = getDayWithEnd(data["dynamic_data"]["day"])

    nextFullMoon = int(calculateFullMoon(data["dynamic_data"]["lunar_day"]))
    #sends messages piecing all this information together
    await message_channel.send("Today's calendar update:\n" + str(currentDate) + ", " + str(writtenDay) + " of " + str(
        currentMonth) + ", " + str(data["dynamic_data"]["year"]))
    await message_channel.send(
        str(calculateMoon(data["dynamic_data"]["lunar_day"])) + ", next full moon is the " + futureDateMonth(
            nextFullMoon) + "\n\nUpcoming Events:\n")
    #prints all the events, if there are no events, prints there is no events
    for event in events:
        await message_channel.send("\n\n" + event + "\n")
    if len(events) == 0:
        await message_channel.send("\nNo upcoming Events" "\n")

    #moves all the dynamic data forward 3 days, checks than nothing cyclical needs to loop back to the beginning
    data["dynamic_data"]["day"] = data["dynamic_data"]["day"] + 3
    if (((data["dynamic_data"]["day"])) % int(
        data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"])) < (
    (data["dynamic_data"]["day"])):

        data["dynamic_data"]["day"] = (((data["dynamic_data"]["day"])) % int(
        data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"]))
        data["dynamic_data"]["timespan"] = data["dynamic_data"]["timespan"] + 1
        if data["dynamic_data"]["day"] == 0:
            data["dynamic_data"]["day"] = data["static_data"]["year_data"]["timespans"][data["dynamic_data"]["timespan"]]["length"]
        if data["dynamic_data"]["timespan"] > 11:
            data["dynamic_data"]["timespan"] = 0
            data["dynamic_data"]["year"] = data["dynamic_data"]["year"] + 1

    data["dynamic_data"]["day_of_week"] = (data["dynamic_data"]["day_of_week"] + 3) % 7

    data["dynamic_data"]["lunar_day"] = (data["dynamic_data"]["lunar_day"] + 3) % 30.5
    #writes all the changes back to the dynamic json
    jsonFile = open("newtest.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()







@getcalender.before_loop
async def before_msg1():  # In order to calculate when the first message should be sent add
    """
    Makes sure the bot is fully connected before running
    """
    await asyncio.sleep(5)
    await client.wait_until_ready()

async def main():
    # Starts the loop
    getcalender.start()

    # start the client
    async with client:
        await client.start(DISCORD_TOKEN)


asyncio.run(main())

