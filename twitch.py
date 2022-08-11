import socket
import threading
import os

SERVER = 'irc.twitch.tv'
PORT = 6667

PASS = os.environ['TWITCH_OATH']

BOT = os.environ['TWITCH_BOT']

CHANNEL = os.environ['TWITCH_CHANNEL']

OWNER = os.environ['TWITCH_OWNER']


message = ""
user = ""
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send((
    "PASS " + PASS + "\n" +
    "NICK " + BOT + "\n" +
    "JOIN #" + CHANNEL + "\n").encode())


def twitch():
    global user
    global message

    def joinChat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024).decode()
            print(readbuffer_join, "!")
            for line in readbuffer_join.split("\n")[0:-1]:
                if "End of /NAMES list" in line:
                    sendMessage(irc, "Online!")
                    Loading = False

    def sendMessage(irc, message):
        msg = "PRIVMSG #" + CHANNEL + " :" + message + "\n"
        irc.send(msg.encode())
    joinChat()

    def getUser(line):
        colons = line.count(":")
        colonless = colons-1
        seperate = line.split(":", colons)
        user = seperate[colonless].split("!", 1)[0]
        return user

    def getMessage(line):
        try:
            message = line.split("PRIVMSG #" + CHANNEL + " :")[1]
        except:
            message = ""
        return message

    def console(line):
        if "PRIVMSG" in line:
            return True
        return False
    irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\n")[0:-1]:
            if line == "":
                continue
            if "PING :tmi.twitch.tv" in line:
                irc.send("PONG :tmi.twitch.tv\r\n".encode())
                continue
            else:
                try:
                    user = getUser(line)
                    message = getMessage(line)
                    print(user + ": " + message)
                except:
                    continue


if __name__ == "__main__":
    t1 = threading.Thread(target=twitch)
    t1.start()
