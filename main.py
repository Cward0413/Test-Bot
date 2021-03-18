import discord
import os
import requests
import json
from replit import db
import random

client = discord.Client()

starterTickers = ["GME", "AMC", "NOK", "BB"]


def getPic():
  response = requests.get("https://inspirobot.me//api?generate=true")
  print(response.text)
  url = response.text
  return(url)

def updateWatchlist(watchlistAdd):
  if "tickers" in db.key():
    tickers = db["tickers"]
    tickers.append(watchlistAdd)
    db["tickers"] = tickers
  else:
    db["tickers"] = [watchlistAdd]  

def deleteWatchlist(index):
  tickers = db["tickers"]
  if len(tickers) > index:
    del tickers[index]
  db["tickers"] = tickers

#https://inspirobot.me//api?generate=true
#https://zenquotes.io/api/random

@client.event
async def on_ready():
  print('test username {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  msgUpper = msg.upper() 
  print(msgUpper)

  if msgUpper == "!INSPIRE":
    pic = getPic()
    print(pic)
    await message.channel.send(pic)

  options = starterTickers
  if "tickers" in db.keys():
    options = + db["tickers"]

  if message.content.startswith('!add'):
    watchlistAdd = msg.split("!add ",1)[1]
    updateWatchlist(watchlistAdd)
    await message.channel.send("Ticker added to watchlist")

  #if message.content.startswith("!del"):
    tickers = []
    if "tickers" in db.keys():
      index = int(msg.split("$del",1)[1])
      deleteWatchlist(index)
      tickers = db["tickers"]
    await message.channel.send(tickers)

client.run(os.getenv('TOKEN'))
  