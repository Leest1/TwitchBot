import socket
import praw
import requests
import json

HOST = "irc.twitch.tv"
PORT = 6667
PASS = "oauth:yacesy8zrh5t6uxf0lce8ntrjke153"
NICK = "posiesenpai"
CHAN = "#thoror"

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))


while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        print(response)

headers = {"Accept": "application/vnd.twitchtv.v3+json"}
url = "https://api.twitch.tv/kraken/channels/thoror"
r = requests.get(url, headers = headers)
gamename = r.json()['game']
print(gamename)
        

s.close()
