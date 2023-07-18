import imdb

ia = imdb.IMDb()
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

print(person("tarantino"))