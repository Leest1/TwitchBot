import socket
import praw
import requests
import json
import time

# variables
HOST = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:nhhmg2fo8mw8t9d1uaqq8y8xft75aj"
NICK = "pilbot"
CHAN = "riotgames"

rusername = "sdhacks"
rpassword = "naruto96"
gamename = ""
useragent = "Twitch Content Creators"

limit = 30

# connects to socket
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN #{}\r\n".format(CHAN).encode("utf-8"))

# sends message to twitch chat
def send_message(chan, msg):
    s.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))

while True:
    # receives response
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        print(response)

    # parses twitch json and gets game name
    headers = {"Accept": "application/vnd.twitchtv.v3+json"}
    url = "https://api.twitch.tv/kraken/channels/" + CHAN
    r = requests.get(url, headers = headers)
    gamename = r.json()['game']
    print(gamename)

    # Reddit login
    r = praw.Reddit(useragent)
    r.login(rusername, rpassword, disable_warning=True)

    # searches Reddit for game name subreddit & gets top threads
    results = r.search(gamename, limit=1)
    for i in results:
        gamename = str(i.subreddit)
    submissions = r.get_subreddit(gamename).get_hot(limit=limit)
    count = 0;

    # sends top threads to twitch chat
    for i in submissions:
        if i.stickied == False:
            send_message("#" + NICK, str(i).replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\u201d", "'"))
            send_message("#" + NICK, i.url)
            count+=1
            time.sleep(20)
        if count == 25:
            break

s.close()
