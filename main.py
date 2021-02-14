import discord
import imdb
import os
from urllib.request import urlretrieve
from keep_alive import keep_alive

client = discord.Client()
ia = imdb.IMDb()
def movie(a):
  b = ia.search_movie(a)[0]
  code = b.movieID
  series = ia.get_movie(code)
  if 'cover url' in series:
    url = series['cover url']
    urlretrieve(url, 'pic.jpg')

  rating = series.data['rating']
  year = series.data['year']
  plot = series.data['plot'][0].split("::")[0]
  cast = [i['name'] for i in series.data['cast'][:3]]
  
  try:
    director = series.data['director'][0]
    str1 = "{0} is a film released in {1} starring {2},{3},{4}.{5}Directed by {6}.\nRating - {7}".format(b,year,cast[0],cast[1],cast[2],plot,director['name'],rating)
  except KeyError:
   str1 = "{0} is a TV show released in {1} starring {2},{3},{4}.{5}\nRating - {6}".format(b,year,cast[0],cast[1],cast[2],plot,rating)
  return str1
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
  if a=='movies':
    t = ia.get_top250_movies()
  if a=='shows':
    t = ia.get_top250_tv()
  if a=='pop':
    t = ia.get_popular100_movies()
  str1=''
  for i in t[:10]:
    str1+='{0}\n'.format(i)
  return str1

@client.event
async def on_ready():
  print("We logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$film"):
      a = message.content[3:]
      result = movie(a)
      await message.channel.send(result)
      await message.channel.send(file=discord.File('pic.jpg'))
    if message.content.startswith("$list"):
      a = message.content[3:]
      result = person(a)
      result = result.replace("()","")
      await message.channel.send(result)
    if message.content.startswith("$top"):
      a = message.content[5:]
      result = top(a)
      await message.channel.send(result)
keep_alive()
client.run(os.getenv("TOKEN"))