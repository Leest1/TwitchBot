import socket
import praw
import requests
import json
import time

HOST = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:yacesy8zrh5t6uxf0lce8ntrjke153"
##PASS = "oauth:7ynekpqi5hxa4e2q8cdi8dlzjo13xu"
NICK = "posiesenpai"
CHAN = "riotgames"

rusername = "sdhacks"
rpassword = "naruto96"
gamename = ""
useragent = "Twitch Content Creators"

limit = 15

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        s.send((":" + NICK + "!" + NICK + "@" + NICK + ".tmi.twitch.tv PRIVMSG #" + CHAN + " :hello").encode("utf-8"))
        headers = {"Accept": "application/vnd.twitchtv.v3+json"}
        url = "https://api.twitch.tv/kraken/channels/" + CHAN
        r = requests.get(url, headers = headers)
        gamename = r.json()['game']
        print(gamename)

        r = praw.Reddit(useragent)
        r.login(rusername, rpassword, disable_warning=True)
        results = r.search(gamename, limit=1)
        for i in results:
            gamename = str(i.subreddit)
        submissions = r.get_subreddit(gamename).get_hot(limit=limit)
        count = 0;
        for i in submissions:
            if i.stickied == False:
                print(str(i).replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\u201d", "'")
                      + "\n" + i.url + "\n")
                count+=1
            if count == 5:
                break
    time.sleep(1200)


s.close()
