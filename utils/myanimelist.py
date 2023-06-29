from utils.helpers.json_generator import malJsonGenerator
from utils.helpers.httpheaders import request_headers
import requests
import urls 

class mal:
  def __init__(self) -> None:
    self.BASE_URL = urls.mal
    
  def topanime(self,page, type):
    params = f"/topanime.php?limit={(int(page)-1)*50}&type={type}"
    data = requests.get(self.BASE_URL+params,headers=request_headers())
    jsonData = malJsonGenerator.topAnimes(data.text,page)
    return (jsonData)
    
  def search(self,q,page):
    url = f"{self.BASE_URL}/anime.php?q={q}&cat=anime&&show={(page-1)*50}"
    data = requests.get(url,headers=request_headers())
    return malJsonGenerator.searchAnime(data,page)
    
  def anime(self,animeid):
    url = f"{self.BASE_URL}/anime/{animeid}"
    data = requests.get(url,headers=request_headers())
    return malJsonGenerator.animeInfo(data,animeid)
  
  def characters(self,animeid):
    url = f"{self.BASE_URL}/anime/{animeid}/animeName/characters"
    data = requests.get(url,headers=request_headers())
    return malJsonGenerator.animeCharacters(data.text,animeid)