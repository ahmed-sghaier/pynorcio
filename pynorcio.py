#!/usr/bin/python
import sys
import socket
import string
import datetime

HOST = "irc.freenode.net"
PORT = 6667
NICK = "pynorcio"
IDENT = "pynorcio"
REALNAME = "Python IRC Bot"
CHANNELS = ["#Neo31", "#pynorcio"]
readbuffer = ""

s = socket.socket()
s.connect((HOST, PORT))

s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

for channel in CHANNELS:
    s.send("JOIN " + channel + " :Hello \r\n")

while 1:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop( )
    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        elif ( (line[1] == "PRIVMSG") and line[3].startswith(":" + NICK) ):
            sndr = line[0]
            rcvr = line[2]
            msg = line[3]
            cmd = line[4]
            rply = ""
            eof = "\r\n"
            if (rcvr.startswith("#")):
                rply = "PRIVMSG " + rcvr + " :"
            else:
                rply = "PRIVMSG " + sndr + " :"
            if (cmd == "ping"):
                s.send(rply + "pong" + eof)
            elif (cmd == "whois"):
                s.send(rply + "My name is " + REALNAME + ", and I am a python IRC bot." + eof)
            elif (cmd == "help"):
                s.send(rply + NICK + " help command (commands : ping, whois)" + eof)
            elif (cmd == "time"):
                s.send(rply + datetime.datetime.now().time().isoformat() + eof)

