import discord
import imdb
import os
from keep_alive import keep_alive
client = discord.Client()
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
  str1 = ia.get_person_filmography(b.personID)
  str2=""
  try:
    for index in range(10):
      movie_name = str1['data']['filmography']['actor'][index]
      str2+="{0}.{1}\n".format(index+1,movie_name)
  except KeyError:
    try :
      for index in range(10):
        movie_name = str1['data']['filmography']['director'][index]
        str2+="{0}.{1}\n".format(index+1,movie_name)
    except KeyError:
      for index in range(10):
        movie_name = str1['data']['filmography']['actress'][index]
        str2+="{0}.{1}\n".format(index+1,movie_name)
  return str2
def top(a):
  if a=='movies': t = ia.get_top250_movies()
  if a=='shows': t = ia.get_top250_tv()
  if a=='popular': t = ia.get_popular100_movies()
  str1=''
  for i in t[:10]: str1+='{0}\n'.format(i)
  return str1

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
      await message.add_reaction("👍")
      a = message.content[3:]
      result = movie(a)
      embedVar = discord.Embed(title=str(result[3]), description=str(result[0]),color=0xF6BE00) 
      embedVar.set_footer(text=result[1])
      embedVar.set_thumbnail(url=result[2])
      await message.channel.send(embed=embedVar)
    if message.content.startswith("$list"):
      await message.add_reaction("👍")
      a = message.content[3:]
      result = person(a)
      result = result.replace("()","")
      embedVar = discord.Embed(title="", description="",color=0xF6BE00)
      embedVar.add_field(name="Filmography", value=result, inline=False)
      await message.channel.send(embed=embedVar)
    if message.content.startswith("$top"):
      await message.add_reaction("👍")
      a = message.content[5:]
      result = top(a)
      if a=="popular":
        a += " movies"
      embedVar = discord.Embed(title="", description="",color=0xF6BE00)
      embedVar.add_field(name="Top {0}".format(a.capitalize()), value=result, inline=False)
      await message.channel.send(embed=embedVar)
    if message.content.startswith("$help"):
        await message.add_reaction("👍")
        embedVar = discord.Embed(title="", description="",color=0xF6BE00)
        embedVar.add_field(name="$film", value="to search about film", inline=False)
        embedVar.add_field(name="$tv", value="to search about tv show", inline=False)
        embedVar.add_field(name="$list", value="to get filmography of a person", inline=False)
        embedVar.add_field(name="$top movies", value="to get top 10 movies", inline=False)
        embedVar.add_field(name="$top shows", value="to get top 10 shows", inline=False)
        embedVar.add_field(name="$top popular", value="to get popular movies", inline=False)
        embedVar.add_field(name="$add", value="to add to Watchlist", inline=False)
        embedVar.add_field(name="$view", value="to view Watchlist", inline=False)
        embedVar.add_field(name="$del", value="to remove from Watchlist", inline=False)
        embedVar.add_field(name="$clear", value="to clear Watchlist", inline=False)
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
      embedVar = discord.Embed(title="", description="",color=0xF6BE00)
      embedVar.add_field(name="Watchlist", value=result, inline=False)
      await message.channel.send(embed=embedVar)
    if message.content.startswith("$clear"):
      f.seek(0)
      await message.add_reaction("👍")
      f.truncate(0)
keep_alive()
client.run(os.getenv("TOKEN"))