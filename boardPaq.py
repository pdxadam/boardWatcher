#notes: 12/29/2023
# It now works
import requests
import bs4
import os
import shelve
import paho.mqtt.publish as publish

broker = "mchome.local"
port = 1883
topic = "homeassistant/rta/board/"



def mqttPost(postable):
    f = open("mq", "r")
    l = f.readline()[:-1].split(",")
    f.close()
    publish.single(topic, payload=postable, hostname=broker, client_id = "boardPoster", port = port, auth = {'username':l[0], 'password':l[1]} )
    
   

#Get the old boardPaq future meetings list
# os.chdir("c:/users/cmsmc/documents/programming/boardWatcher")
os.chdir("/home/gandalf/boardWatcher")

filename = "oldBoardMeetings"
siteAddress = "https://www.boardpaq.com/cast?c=hG3yQ4gP3kN6yH7uJ5sB&t=N"
try:
    p = shelve.open(filename)
    old = p['oldBoardMeetings']
    p.close()
except KeyError:
    old = ""

#Get the current boardPaq future meetings list
res = requests.get("https://www.boardpaq.com/cast?c=hG3yQ4gP3kN6yH7uJ5sB&t=N")
res.raise_for_status()
boardSoup = bs4.BeautifulSoup(res.text, 'html.parser')
futureMeetings = str(boardSoup.select('table#mdtbl')[0])
if (futureMeetings == old):
    print("It's all the same and there's nothing you can do about it.")
else:
    print(futureMeetings)
    p = shelve.open(filename)
    p['oldBoardMeetings'] = futureMeetings
    p.close()
    #This is where I want to send the email out.
    mqttPost(futureMeetings)




  


