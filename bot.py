import discord
import responses
import requests
import xmltodict

async def send_message(message, user_message):
    try:
        response = handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = "NzcyMTU2NTk2NzgwMjY5NTY4.G7pSe4.EoirHyWQyTKjuHismpBx9h1OCjk598ldx0tNG4"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if user_message[0] == "/":
            print(f"{username} did a weather request")
            user_message = user_message[1:]
            await send_message(message, user_message)

    client.run(TOKEN)

#**************************************************************************************************
# Formating data
#**************************************************************************************************

def handle_response(message):
    p_message = message.lower()

    if p_message == "weather":
        return weather_report()

def weather_report():
    url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    parameters = []
    parameters.append(data["dwml"]["data"]["time-layout"]["start-valid-time"][:167])
    parameters.append(data["dwml"]["data"]["parameters"]["cloud-amount"]["value"][:167])
    parameters.append(data["dwml"]["data"]["parameters"]["probability-of-precipitation"]["value"][:167])

    print(parameters)
    return "yep"