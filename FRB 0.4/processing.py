#processing

import urllib.request
import json

url = 'https://orion.shoutca.st/rpc/flareradio/streaminfo.get'

def readData():
    while True:
        try:
            ok = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))["data"][0]
        except:
            continue
        return ok
        break

def getStat():
  data = readData()
  return str(data["track"]["title"])+" by "+ str(data["track"]["artist"])

def getDJ():
  return readData()["title"]

def oldDJ():
  f = open("DJ.data","r")
  DJ = f.read()
  f.close()
  return DJ

def setDJ():
  f = open("DJ.data","w")
  f.write(getDJ())
  f.close()

def getChannel(id):
  f = open(id+".data","r")
  channel_id = int(f.read())
  f.close()
  return channel_id

def getVoice(id):
  f = open(id+"_voice.data","r")
  voice_id = f.read()
  f.close()
  return voice_id
