import irc.client
import os
import time
import pickle
import random
from settings import *
from responses import *
reactor = irc.client.Reactor()
irc.client.ServerConnection.buffer_class.encoding = "UTF-8"
irc.client.ServerConnection.buffer_class.errors = "replace"
loopin = 0
theresaduck = 0
start_time = 0
ducklines = 0
ducktime = 0
scoreboard = {}
missed = {}

if os.path.isfile("duckhunt.pkl") == False:
    open("duckhunt.pkl", 'w').close()

if "!bang" not in scoreboard:
    scoreboard["!bang"] = {}
if "!bef" not in scoreboard:
    scoreboard["!bef"] = {}

def stoploop():
    global loopin
    loopin = 0

def get_word(cmd):
    if cmd == "!bang":
        return {"present": "shoot", "past": "shot"}
    else:
        return {"present": "befriend", "past": "befriended"}

def random_response(cmd, shooter):
    if cmd == "!bang":
        cmdresponse = bangmisses
    else:
        cmdresponse = befmisses
    cmdlen = len(cmdresponse) - 1
    picked_response = cmdresponse[random.randint(0,cmdlen)] % (shooter)
    return picked_response

def save_scores():
    global scoreboard
    with open('duckhunt.pkl', 'wb') as fp:
        pickle.dump(scoreboard, fp)

def add_score(shooter, cmd, score):
    global scoreboard
    if shooter not in scoreboard["!bang"]:
        scoreboard["!bang"][shooter] = 0
    if shooter not in scoreboard["!bef"]:
        scoreboard["!bef"][shooter] = 0
    totalcmd = "total" + cmd
    if not totalcmd in scoreboard["stats"]:
         scoreboard["stats"][totalcmd] = 0
    scoreboard["stats"][totalcmd] += 1
    scoreboard[cmd][shooter] += score
    save_scores()

def del_score(player):
    global scoreboard
    scoreboard["!bang"].pop(player)
    scoreboard["!bef"].pop(player)
    time.sleep(2)
    save_scores()

def load_scores():
    global scoreboard
    global DUCKLINES_TARGET
    if os.path.getsize('duckhunt.pkl') > 0:
        with open('duckhunt.pkl', 'rb') as fp:
            scoreboard = pickle.load(fp)
    if "ducklines" in scoreboard:
        DUCKLINES_TARGET = scoreboard["ducklines"]
    if "MISS_CHANCE" in scoreboard:
        MISS_CHANCE = scoreboard["MISS_CHANCE"]
    if "stats" not in scoreboard:
        scoreboard["stats"] = {}
        scoreboard["stats"]["totalmissed"] = 0
        scoreboard["stats"]["!bangmissed"] = 0
        scoreboard["stats"]["!befmissed"] = 0
        scoreboard["stats"]["total!bang"] = 0
        scoreboard["stats"]["total!bef"] = 0
        save_scores()
        time.sleep(1)
    print("Scores loaded!")
    print(scoreboard)

def inbold(s):
    return "\x02" + s + "\x02"

def on_connectbot(connection, event):
    print("Connection successfull")
    connection.join(CHANNEL)

def on_nicknameinuse(connection, event):
    nick = connection.get_nickname()
    newnick = nick + "_"
    print(nick + " is in use. Retrying with " + newnick)
    connection.nick(newnick)

def on_join(connection, event):
    if connection.get_nickname() == event.source.nick:
        print("Joined", event.target)
        connection.privmsg(event.target, "The DuckHunt Begins!")

def on_pubmsg(connection, event):
    global theresaduck
    global ducklines
    global ducktime
    global DUCKLINES_TARGET
    global MISS_CHANCE
    global missed
    if len(event.arguments[0].split()) == 0:
        return
    channel = event.target
    print(event.source.nick + ":", event.arguments[0])
    msg = event.arguments[0].split()
    msg[0] = msg[0].lower()
    if theresaduck == 0:
        ducklines += 1
    if ducklines >= DUCKLINES_TARGET and theresaduck != 1:
        theresaduck = 1
        ducklines = 0
        ducktime = time.time()
        connection.privmsg(channel, "・゜゜・。 ​ 。・゜゜\_ø<​ FLAP F​LAP!")
        return
    if msg[0] == "!befriend":
        msg[0] = "!bef"
    bangbef = ["!bang", "!bef"]
    conds = [msg[0] == "!bang", msg[0] == "!bef"]
    if any(conds):
        cmd = bangbef[conds.index(True)]
        word = get_word(cmd)
        if theresaduck:
            shooter = event.source.nick
            if shooter in missed:
                timemiss = round(time.time(), 0)
                timemissdiff = timemiss - missed[shooter]
                if timemissdiff < 7:
                    return
            rand = random.randrange(1,100)
            if rand < MISS_CHANCE:
                response = random_response(msg[0], shooter)
                connection.privmsg(channel, "MISS! " + response)
                missed[shooter] = round(time.time(),0)
                scoreboard["stats"][cmd + "missed"] += 1
                scoreboard["stats"]["totalmissed"] += 1
                cmdshootermissed = cmd + shooter + "missed"
                if not cmdshootermissed in scoreboard["stats"]:
                     scoreboard["stats"][cmdshootermissed] = 0
                scoreboard["stats"][cmdshootermissed] += 1
                save_scores()
                return
            timeshot = time.time()
            theresaduck = 0
            timediff = round(timeshot - ducktime, 3)
            add_score(shooter, cmd, 1)
            score = scoreboard[cmd][shooter]
            missed = {}
            connection.privmsg(channel, "Congrats " + shooter + " you " + word["past"] + " the duck in " + str(timediff) + " seconds! You have " + word["past"] + " " + str(score) + " ducks in " +  channel + ".")
        else:
            connection.privmsg(channel, "There is no duck to " +  word["present"])
    if msg[0] == "!allstats":
        stats = scoreboard["stats"]
        if "!bangmissed" not in stats:
             bangmissed = 0
        else:
             bangmissed = scoreboard["stats"]["!bangmissed"]
        if "!befmissed" not in stats:
             befmissed = 0
        else:
             befmissed = scoreboard["stats"]["!befmissed"]
        if "totalmissed" not in stats:
             totalmissed = 0
        else:
             totalmissed = scoreboard["stats"]["totalmissed"]
        statsline = "%s: %s | %s: %s | %s: %s | %s: %s | %s: %s"  % (inbold("Successful shots"), scoreboard["stats"]["total!bang"], inbold("Succesful friendsips"), scoreboard["stats"]["total!bef"], inbold("Missed shots"), bangmissed, inbold("Missed friendships"), befmissed, inbold("Total missed"), totalmissed)
        connection.privmsg(channel, statsline)
    elif msg[0] == "!stats":
         stats = scoreboard["stats"]
         bang = scoreboard["!bang"]
         bef = scoreboard["!bef"]
         if len(msg) == 1:
             nick = event.source.nick
         else:
             nick = msg[1]
         bangshootermissed = "!bang" + nick + "missed"
         if not bangshootermissed in scoreboard["stats"]:
              nickbangmissed = 0
         else:
              nickbangmissed = scoreboard["stats"][bangshootermissed]
         befshootermissed = "!bef" + nick + "missed"
         if not befshootermissed in scoreboard["stats"]:
              nickbefmissed = 0
         else:
              nickbefmissed = scoreboard["stats"][befshootermissed]
         if not nick in bang:
              nickbanged = 0
         else:
              nickbanged = scoreboard["!bang"][nick]
         if not nick in bef:
              nickbefed = 0
         else:
              nickbefed = scoreboard["!bef"][nick]
         statsline = "%s stats: %s: %s | %s: %s | %s: %s | %s: %s" % (nick, inbold("Successful shots"), nickbanged, inbold("Successful friendships"), nickbefed, inbold("Missed shots"), nickbangmissed, inbold("Missed friendships"), nickbefmissed)
         connection.privmsg(channel, statsline)
    elif msg[0] == "!killers":
        s = ""
        x = {k: v for k, v in sorted(scoreboard["!bang"].items(), key=lambda item: item[1], reverse=True)}
        for p in x:
            if x[p] > 0:
                s += "\x02" + p + "\x0f: " + str(x[p]) + " "
        connection.privmsg(channel, "Killers in " + channel + ": " + s)
    elif msg[0] == "!friends":
        s = ""
        x = {k: v for k, v in sorted(scoreboard["!bef"].items(), key=lambda item: item[1], reverse=True)}
        for p in x:
            if x[p] > 0:
                s += "\x02" + p + "\x0f: " + str(x[p]) + " "
        connection.privmsg(channel, "Friends in " + channel + ": " + s)
    elif msg[0] == "!ducks":
        if len(msg) == 1:
            whoseducks = event.source.nick
            wordduck = ", you have"
        else:
            whoseducks = msg[1]
            wordduck = " has"
        if whoseducks in scoreboard["!bang"]:
            killed = scoreboard["!bang"][whoseducks]
            friended = scoreboard["!bef"][whoseducks]
            if killed > 0 or friended > 0:
                connection.privmsg(channel, whoseducks + wordduck + " killed " + str(killed) + " and befriended " + str(friended) + " ducks in " + channel)
            else:
                connection.privmsg(channel, whoseducks + wordduck + "n't killed or befriended any ducks in " + channel)
        else:
            connection.privmsg(channel, whoseducks + ": No such nick in my scoreboard!")
    if event.source.nick in duckops:
        if msg[0] == "!duckdown":
            connection.quit("It was " + event.source.nick + ", he pressed the red button! Agh! *dead*")
            stoploop()
        elif msg[0] == "!ducklines":
            if len(msg) == 1:
                connection.privmsg(channel, "The current ducklines setting is " + str(DUCKLINES_TARGET))
                return
            if msg[1].isnumeric() == False:
                connection.privmsg(channel, "I need a number, dummy.")
                return
            DUCKLINES_TARGET = int(msg[1])
            scoreboard["ducklines"] = DUCKLINES_TARGET
            save_scores()
            connection.privmsg(channel, "The ducks will now spawn after " + msg[1] + " lines.")
        elif msg[0] == "!merge":
            if len(msg) < 3:
                connection.privmsg(channel, "Usage: !merge from-nick to-nick")
                return
            tomovebang = 0
            tomovebef = 0
            if msg[1] in scoreboard["!bang"]:
                tomovebang = scoreboard["!bang"][msg[1]]
                add_score(msg[2], "!bang", tomovebang)
                tomovebef = scoreboard["!bef"][msg[1]]
                add_score(msg[2], "!bef", tomovebef)
                del_score(msg[1])
                connection.privmsg(channel, "Moved " + str(tomovebang) + " dead ducks and " + str(tomovebef) + " befriended ducks from " + msg[1] + " to " + msg[2])
            else:
                connection.privmsg(channel, msg[1] + ": No such nick in my scoreboard.")
        elif msg[0] == "!misschance":
            if len(msg) == 1 or msg[1].isnumeric() == False or (msg[1].isnumeric() == True and int(msg[1]) not in range(1,101)):
                connection.privmsg(channel, "Usage: !misschance " + str(random.randrange(1,100)))
                return
            MISS_CHANCE = int(msg[1])
            connection.privmsg(channel, "Miss chance set to " + msg[1])
            scoreboard["MISS_CHANCE"] = MISS_CHANCE
            save_scores()

def on_disconnect(connection, event):
    print(event.source, event.arguments[0])
    stoploop()

def startloop():
    print("Starting the bot, loading scores...")
    global start_time
    start_time = int(time.time())
    load_scores()
    try:
        con = reactor.server().connect(SERVER, PORT, NICK, None, "Quack", "Kill the ducks")
    except irc.client.ServerConnectionError:
        print(irc.client.ServerConnectionError)
        return
    reactor.add_global_handler("welcome", on_connectbot)
    reactor.add_global_handler("join", on_join)
    reactor.add_global_handler("pubmsg", on_pubmsg)
    reactor.add_global_handler("disconnect", on_disconnect)
    reactor.add_global_handler("nicknameinuse", on_nicknameinuse)
    global loopin
    loopin = 1
    time.sleep(2)
    while loopin:
        reactor.process_once(0.2)
        time.sleep(0.2)

startloop()

