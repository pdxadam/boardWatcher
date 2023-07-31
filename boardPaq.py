import requests
import bs4
import os
import shelve
import ezgmail

ezgmail.init()

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



    ezgmail.send("pdxadam@gmail.com", "Changes to upcoming board meetings", siteAddress + "\n" + futureMeetings)


