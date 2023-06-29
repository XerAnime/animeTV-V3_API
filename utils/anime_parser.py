from utils.helpers.json_generator import zoroJsonGenerator, gogoJsonGenerator
from utils.helpers.httpheaders import request_headers
from bs4 import BeautifulSoup
import requests
import urls
import json

## sanji.to
class sanji:
  def __init__(self) -> None:
    self.BASE_URL = urls.sanji
    
  def search(self, query):
    data = requests.get(f"{self.BASE_URL}/search?keyword={query}")
    soup = BeautifulSoup(data.text,"html.parser")
    return zoroJsonGenerator.searchJson(soup,self.BASE_URL)

  def anime(self,id):
    data = requests.get(self.BASE_URL+"/"+id)
    soup = BeautifulSoup(data.text,"html.parser")
    return zoroJsonGenerator.animeJson(soup)

## gogoanime
class gogo:
  def __init__(self) -> None:
    self.BASE_AJAX_URL = urls.gogo_ajax
    self.BASE_URL = urls.gogo1
  
  def search(self,query):
    data = requests.get(f"{self.BASE_AJAX_URL}/site/loadAjaxSearch?keyword={query}")
    soup = BeautifulSoup(json.loads(data.text)["content"],"html.parser")
    return gogoJsonGenerator.searchJson(soup)

  def anime(self, gogoid):
    data = requests.get(f"{self.BASE_URL}/category/{gogoid}", headers=request_headers())
    soup = BeautifulSoup(data.text, "html.parser")
    id = soup.select("#movie_id")[0]["value"]
    name = soup.select("#alias_anime")[0]["value"]
    episData = requests.get(f"{self.BASE_AJAX_URL}/ajax/load-list-episode?ep_start=0&ep_end=9999&id={id}&alias={name}",headers=request_headers())
    episSoup = BeautifulSoup(episData.content, 'html.parser')
    return gogoJsonGenerator.animeJson(soup,episSoup)
  
  def episode(self,gogoEpId):
    data = requests.get(f"{self.BASE_URL}/{gogoEpId}",headers=request_headers())
    soup = BeautifulSoup(data.text,"html.parser")
    return gogoJsonGenerator.episodeJson(soup) 