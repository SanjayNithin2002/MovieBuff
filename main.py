import discord
import imdb
import os
from keep_alive import keep_alive

intents = discord.Intents.default() 
intents.message_content = True
client = discord.Client(intents=intents)
ia = imdb.IMDb()

def movie(a):
  b = ia.search_movie(a)[0]
  code = b.movieID
  series = ia.get_movie(code)
  if 'cover url' in series: url = series['cover url']
  cast = ",".join([str(i) for i in series.data['cast'][:3]])
  rating = cast + "\n" + str(series.data['rating']) +"\n" + str(series.data['year'])
  plot = series.data['plot'][0].split("::")[0]
  return (rating,plot,url,b)

def person(a):
  b = ia.search_person(a)[0]
  print(b)
  str1 = ia.get_person_filmography(b.personID)
  str2=""
  index = 0
  try:
    for movie_name in str1['data']['filmography']['director']:
      index+=1
      if index == 11: break
      str2+="{0}.{1}\n".format(index,movie_name["title"])
  except KeyError:
    try :
      for movie_name in str1['data']['filmography']['actor']:
        index+=1
        if index == 11: break
        str2+="{0}.{1}\n".format(index,movie_name["title"])

    except KeyError:
      for movie_name in str1['data']['filmography']['actress']:
        index+=1
        if index == 11: break
        str2+="{0}.{1}\n".format(index,movie_name["title"])
  return str2

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))

@client.event
async def on_message(message):
    
    file = str(message.guild.id) + ".txt"
    f= open(file,"a+")
    if message.author == client.user:
        return
    
    if message.content.startswith("$film") or message.content.startswith("$tv"):
      a = message.content[3:]
      result = movie(a)

      if result: 
          await message.add_reaction("👍")
          embedVar = discord.Embed(title=str(result[3]), description=str(result[0]),color=0xC8E6C9) 
          embedVar.set_footer(text=result[1])
          embedVar.set_thumbnail(url=result[2])
          await message.channel.send(embed=embedVar)
           
      else:
          await message.add_reaction("👎")
          embed = discord.Embed(title="Page Unavailable", description="Try different prompt.", color=0xFFCDD2)
          await message.channel.send(embed=embed)


    if message.content.startswith("$list"):
      a = message.content[3:]
      result = person(a)
      result = result.replace("()","")

      if result: 
          await message.add_reaction("👍")
          result = result.replace("()","")
          embedVar = discord.Embed(title="", description="",color=0xC8E6C9)
          embedVar.add_field(name="Filmography", value=result, inline=False)
          await message.channel.send(embed=embedVar)
           
      else:
          await message.add_reaction("👎")
          embed = discord.Embed(title="Page Unavailable", description="Try different prompt.", color=0xFFCDD2)
          await message.channel.send(embed=embed)

    if message.content.startswith("$help"):
        await message.add_reaction("👍")
        embedVar = discord.Embed(title="", description="",color=0xC8E6C9)
        embedVar.add_field(name="$film", value="to search about a film", inline=False)
        embedVar.add_field(name="$tv", value="to search about a tv show", inline=False)
        embedVar.add_field(name="$list", value="to get the filmography of a person", inline=False)
        embedVar.add_field(name="$add", value="to add to watchlist", inline=False)
        embedVar.add_field(name="$view", value="to view watchlist", inline=False)
        embedVar.add_field(name="$del", value="to remove from watchlist", inline=False)
        embedVar.add_field(name="$clear", value="to clear watchlist", inline=False)
        await message.channel.send(embed=embedVar)

    if message.content.startswith("$add"):
      f.seek(0)
      await message.add_reaction("👍")
      a = message.content[4:]
      a = str(ia.search_movie(a)[0]) + "\n"
      if a in f.readlines() : pass
      else : f.write(a)

    if message.content.startswith("$del"):
      f.seek(0) 
      await message.add_reaction("👍")
      a = message.content[4:]
      a = str(ia.search_movie(a)) + "\n"
      temp = f.readlines()
      temp = [i for i in temp if i!=a]
      f.truncate(0)
      for i in temp: f.write(i)

    if message.content.startswith("$view"):
      f.seek(0)
      await message.add_reaction("👍")
      a = [i.replace("\n",'') for i in f.readlines()]
      result = "\n".join(a)
      if result=="": result="None"
      embedVar = discord.Embed(title="", description="",color=0xC8E6C9)
      embedVar.add_field(name="Watchlist", value=result, inline=False)
      await message.channel.send(embed=embedVar)

    if message.content.startswith("$clear"):
      f.seek(0)
      await message.add_reaction("👍")
      f.truncate(0)

keep_alive()


bot_token = os.getenv("TOKEN")
if bot_token:
    client.run(bot_token)
else:
   print("The bot token is invalid.")