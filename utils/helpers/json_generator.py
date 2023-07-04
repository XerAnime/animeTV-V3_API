from bs4 import BeautifulSoup
import json

class zoroJsonGenerator:
  def __init__(self) -> None:
    pass
  
  def searchJson(soup,url):
    IMG = [a["data-src"] for a in soup.select(".flw-item .film-poster img.film-poster-img")]
    LINK = [url+a["href"] for a in soup.select(".film-poster-ahref")]
    TITLES = [a["title"] for a in soup.select(".film-poster-ahref")]
    DETAILS = soup.select(".flw-item .film-detail")
    TYPE = [x.select("span")[0].text for x in DETAILS]
    DURATION = [x.select("span")[2].text for x in DETAILS]
    json_data = "["
    for i in range(len(IMG)):
      json_data += '{"title":"'+TITLES[i]+'","thumbnail":"'+IMG[i]+'","id":"'+LINK[i].replace("https://sanji.to/","").replace("?ref=search","")+'","type":"'+TYPE[i]+'","duration":"'+DURATION[i]+'"},'
    return json.loads(json_data[:-1]+"]")
  
  def animeJson(soup):
    info = {
    "title": soup.select(".anisc-detail .film-name")[0].text,
    "japanese": soup.select(".anisc-info .item-title .name")[0].text,
    "quality": soup.select(".anisc-detail .tick-quality")[0].text,
    "dub": soup.select(".anisc-detail .tick-dub")[0].text,
    "sub": soup.select(".anisc-detail .tick-sub")[0].text,
    "episodes": soup.select(".anisc-detail .tick-eps")[0].text,
    "type": soup.select(".anisc-detail .item")[0].text,
    "duration": soup.select(".anisc-detail .item")[1].text,
    "thumbnail": soup.select(".film-poster-img")[0]["src"],
    "description": soup.select(".anisc-info .item-title .text")[0].text.strip(),
    "aired": soup.select(".anisc-info .item-title .name")[1].text,
    "premiered": soup.select(".anisc-info .item-title .name")[2].text,
    "duration": soup.select(".anisc-info .item-title .name")[3].text,
    "status": soup.select(".anisc-info .item-title .name")[4].text,
    "malScore": soup.select(".anisc-info .item-title .name")[5].text,
    "genres": [{"title": x["title"], "url": x["href"]} for x in soup.select(".anisc-info .item-list a")],
    "studios": [{"name" : x.text, "url": x["href"]} for x in soup.select(".anisc-info .item-title")[7].select("a")],
    "producers": [{"name" : x.text, "url": x["href"]} for x in soup.select(".anisc-info .item-title")[8].select("a")],
    }
    return json.dumps(info, indent = 2)

class gogoJsonGenerator():
  def __init__(self) -> None:
    pass
  def searchJson(soup): 
    titles = [x.text for x in soup.select(".ss-title")]
    thumbnail = [(x["style"])[17:-2] for x in soup.select(".ss-title div")]
    gogoId =[x["href"] for x in soup.select(".ss-title")]
    json_data = "["
    for i in range(len(titles)):
      json_data += '{"title":"'+titles[i]+'","thumbnail":"'+thumbnail[i]+'","id": "'+gogoId[i].replace("category/","")+'"},'
    return json.loads(json_data[:-1]+"]")
  
  def animeJson(html,epis):
    eparr = [x["href"].replace(" /","") for x in epis.select("a")][::-1]
    genre = html.select(".anime_info_body .type")[2].select("a")
    status = html.select(".anime_info_body .type")[4]
    info = {
      "title": html.select(".anime_info_body h1")[0].text,
      "thumbnail": html.select(".anime_info_body img")[0]["src"],
      "type": html.select(".anime_info_body .type")[0].text.split("\n")[1],
      "description": html.select(".anime_info_body .type")[1].text.replace("Plot Summary: ",""),
      "genre": [{"title":a["title"], "url": "genre/"+a["href"].split("/genre/")[1]} for a in genre],
      "released" : html.select(".anime_info_body .type")[3].text.replace("Released: ",""),
      "status" : {"title": status.select("a")[0]["title"],"url" : status.select("a")[0]["href"]},
      "other_name" : html.select(".anime_info_body .type")[5].text.replace("Other name: ",""),
      "episodes": eparr
    }
    return json.dumps(info)
  def episodeJson(soup):
    servers = [{"video": x["data-video"],"name": x.text.replace("Choose this server","").replace("\n","")} for x in soup.select(".anime_muti_link ul li a")]
    return json.dumps(servers, indent = 2)

## myanimelist.net ##
class malJsonGenerator:
  def __init__(self) -> None:
    pass

  def searchAnime(data,page):
    soup = BeautifulSoup(data.text, "html.parser")
    last_page = 20 # int(soup.select(".ac .spaceit .bgColor1 a")[-1].text)
    animes = soup.select("#content div.list table tr")
    del animes[0]
    dataDict = {
      "pagination":{
        "next_page": True if page < last_page else False,
        "prev_page": True if page > 1 else False,
        "page": page
      },
      "items": [
        {
          "title": anime.select(".title a")[0].text,
          "mal_id": int(anime.select(".picSurround a")[0]["href"].replace("https://myanimelist.net/anime/","").split("/")[0]),
          "type": anime.select(".ac")[0].text.strip(" \n"),
          "url": anime.select(".picSurround a")[0]["href"],
          "img": (anime.select(".picSurround img")[0]["data-srcset"].split(" 1x, ")[1].replace(" 2x","")),
          "score": (anime.select(".ac")[2].text.strip(" \n"))
        } for anime in animes
      ]
    }
    return json.dumps(dataDict)


  def topAnimes(data,page):
    soup = BeautifulSoup(data,"html.parser")
    next = soup.select(".pagination .next")
    prev = soup.select(".pagination .prev")
    pagination = {
      "next_page": (False if len(next) == 0 else True),
      "prev_page": (False if len(prev) == 0 else True),
      "page": page
    }
    animes = soup.select(".ranking-list")
    data_dict = {
      "pagination" : pagination,
      "items": [
        {
          "title": anime.select(".anime_ranking_h3")[0].text,
          "mal_id": anime.select("a")[0]["href"].replace("https://myanimelist.net/","").split("/")[1],
          "type": anime.select("a")[0]["href"].replace("https://myanimelist.net/","").split("/")[0],
          "url": anime.select("a")[0]["href"],
          "img": (anime.select("img")[0]["data-srcset"].split(", ")[1]).replace(" 2x",""),
          "rank": anime.select(".top-anime-rank-text")[0].text
        } for anime in animes
      ]
    }
    return json.dumps(data_dict)
  
  def animeInfo(data, malid):
    soup = BeautifulSoup(data.text,"html.parser")
    songsarr = []
    for x in soup.select(".di-tc table tr"):
      if len(x.select("td")) != 3:
        pass
      else:
        song = (x.select("td"))[1].select("input")
        songsarr.append(song)
    # print(songsarr)
    songs = []
    for x in songsarr:
       if len(x) != 0 and x[0]["value"] != "":
        songs.append(x[0]["value"].split("/track/")[1])   
    infoDict = {
      "title": soup.select(".title-name")[0].text,
      "mal_id":  malid,
      "rank": soup.select(".stats-block .ranked strong")[0].text,
      "popularity": soup.select(".stats-block .popularity strong")[0].text,
      "score": soup.select(".stats-block .score")[0].text,
      "img": soup.select(".borderClass .leftside img")[0]["data-src"],
      "description": soup.findAll("p", {"itemprop" : "description"})[0].text, 
      "info": {x.select(".dark_text")[0].text.replace(":","").strip().lower() : x.text.replace(x.select('.dark_text')[0].text,"").strip() for x in soup.select(".borderClass .leftside .spaceit_pad")},
      "external_links": [{"name": x.text.strip().lower(), "data" : x["href"]} for x in soup.select(".external_links a")],
      "theme_songs": songs
    }
    return json.dumps(infoDict)
  
  def animeCharacters(data,malid):
    soup = BeautifulSoup(data,"html.parser")
    charactersList = soup.select(".anime-character-container table tr")
    x = []
    for character in charactersList:
      cName = character.select(".js-chara-roll-and-name")
      if len(cName) != 0:
        voice_actors = character.select(".js-anime-character-va .js-anime-character-va-lang")
        cINfoJson ={
          "name" : cName[0].text.strip(" \n").split("_")[1],
          "img": str(character.select(".ac img")[0]["data-srcset"].split(" 1x, ")[1].replace(" 2x","")),
          "type" : "main" if cName[0].text.strip(" \n").split("_")[0] == "m" else "supporting",
          "voice_actors" : [{
            "name": x.select('td')[0].select(".spaceit_pad")[0].text.strip("\n"),
            "img": x.select('td')[1].select("img")[0]["data-srcset"].split(", ")[1].replace(" 2x",""),
            "lang" : x.select(".js-anime-character-language")[0].text.strip("\n ") 
                }for x in voice_actors]}
        x.append(cINfoJson)
    charactersInfo = {
      "mal_id": malid,
      "name": soup.select(".title-name")[0].text,
      "data": (x)
    }
    return json.dumps(charactersInfo)
