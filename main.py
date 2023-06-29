from utils.anime_parser import gogo
from utils.myanimelist import mal
from flask import Flask,request
from flask_cors import CORS
from utils.vidstreaming import getEpStreamingLink
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def home(): 
  return "<html style='background: #000; color:#fff'><br><h2>⚒ AnimeTV-V3_API ⚒ </h2></html>"

@app.route("/search/<site>")
def search(site):
  query = request.args.get("q")
  if site == "gogoanime":
    return  gogo().search(query)

@app.route("/episodes/<site>/<animeid>")
def episodes(site,animeid):
  if site == "gogoanime":
    return json.loads(gogo().anime(animeid))

@app.route("/episode/<site>/<epid>")
def episode(site,epid):
  if site == "gogoanime":
    return json.loads(gogo().episode(epid))

##    MyAnimeList   ##
@app.route("/search")
def malSearch():
  query = request.args.get("q")
  page = request.args.get("page")
  searchJson = mal().search(query,int(page))
  return json.loads(searchJson)

@app.route("/topanime")
def topAnime():
  query = request.args.get("page")
  type = request.args.get("type")  ## airing & favorite & bypopularity
  topAnimeJson = mal().topanime(query, type)
  return json.loads(topAnimeJson)

@app.route("/anime/<animeid>")
def malAnime(animeid):
  return json.loads(mal().anime(animeid))

@app.route("/anime/<animeid>/characters")
def charactersinfo(animeid):
  return json.loads(mal().characters(animeid))

##  extract vidstreaming link  ##
@app.route("/episode/streaminglink/vidstreaming")
def getVidstreamingEmbedLink():
  iframe = request.args.get("iframeUrl")
  return getEpStreamingLink(iframe)

if __name__ == "__main__":
  app.run(debug=True,host="0.0.0.0")