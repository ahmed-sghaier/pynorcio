#!/usr/bin/python
import sys
import socket
import string
import datetime
import config as config

class Pynorcio:
    readbuffer = ""
    s = ""
    conf = ""

    def __init__(self):
        self.conf = config.Config()
        self.connect()

    def connect(self):
        self.s = socket.socket()
        self.s.connect((self.conf.HOST, self.conf.PORT))
        self.s.send("NICK %s\r\n" % self.conf.NICK)
        self.s.send("USER %s %s bla :%s\r\n" % (self.conf.IDENT, self.conf.HOST, self.conf.REALNAME))
        for channel in self.conf.CHANNELS:
            self.s.send("JOIN " + channel + "\r\n")
        while 1:
            self.readbuffer = self.readbuffer + self.s.recv(1024)
            temp = string.split(self.readbuffer, "\n")
            self.readbuffer = temp.pop( )
            for line in temp:
                msg = line
                line = string.rstrip(line)
                line = string.split(line)
                if (line[0] == "PING"):
                    self.s.send("PONG %s\r\n" % line[1])
                elif ( (line[1] == "PRIVMSG") and line[3].startswith(":" + self.conf.NICK) ):
                    self.read(line, msg)

    def read(self, line, msg):
        sndr = line[0][1:line[0].find("!")]
        rcvr = line[2]
        rply = ""
        cmd = line[4]
        to = ""
        if (rcvr.startswith("#")):
            to = rcvr
        else:
            to = sndr
        if (cmd == "ping"):
            self.write(to, self.query(line, msg))
        elif (cmd == "whois"):
            self.write(to, self.query(line, msg))
        elif (cmd == "help"):
            self.write(to, self.query(line, msg))
        elif (cmd == "time"):
            self.write(to, self.query(line, msg))

    def write(self, to, output):
        for line in output:
            self.s.send("PRIVMSG " + to + " :" + line + "\r\n")
        return ""

    def query(self, line, msg):
        sndr = line[0][1:line[0].find("!")]
        rcvr = line[2]
        cmd = line[4]
        msg = msg[string.find(msg, ":", 1)+1:]
        rply = []
        eof = "\r\n"
        if (cmd == "ping"):
            return ["pong"]
        elif (cmd == "whois"):
            return ["My name is " + self.conf.REALNAME + ", and I am a python IRC bot."]
        elif (cmd == "help"):
            return [self.conf.NICK + " help command (commands : ping, whois)"]
        elif (cmd == "time"):
            return [datetime.datetime.now().time().isoformat()]

if __name__ == '__main__':
    bot = Pynorcio()

