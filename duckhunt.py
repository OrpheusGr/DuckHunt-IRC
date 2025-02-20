import irc.client
import re
import os
import time
import pickle
import random
from settings import *
from responses import *
import thetimers
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
MISS_CHANCE = 0
snipe_dir = 0
cooldown = {}
last_duck = 0
last_duck_player = ""

# Hello world!

if os.path.isfile("duckhunt.pkl") == False:
    open("duckhunt.pkl", 'w').close()

scoreboard["stats"] = {}
if "!bang" not in scoreboard:
    scoreboard["!bang"] = {}
if "!bef" not in scoreboard:
    scoreboard["!bef"] = {}
if "!bangmissed" not in scoreboard["stats"]:
    scoreboard["stats"]["!bangmissed"] = 0
if "!befmissed" not in scoreboard["stats"]:
    scoreboard["stats"]["!befmissed"] = 0

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

def split_msg(msg, max_chars):
    piece = ""
    all_pieces = []
    msgsplit = re.split('\s+(?=\x1d)', msg)
    if len(msgsplit) == 1 and len(msgsplit[0]) > max_chars:
        msgsplit = [msgsplit[0][0:max_chars], msgsplit[0][max_chars:]]
    i = 0
    while i < len(msgsplit):
        if piece != "":
            to_be_piece = piece + " " + msgsplit[i]
        else:
            to_be_piece = piece + msgsplit[i]
        if len(piece) <= max_chars and len(to_be_piece) <= max_chars:
            piece = to_be_piece
        else:
            if piece == "":
                msgsplit = msgsplit[0:i-1] + [to_be_piece[0:max_chars], to_be_piece[max_chars:]] + msgsplit[i+1:]
                piece = msgsplit[i-1]
            all_pieces.append([piece])
            piece = ""
            i -= 1
        i += 1
    all_pieces.append([piece])
    return all_pieces

def score_output(score_dict, friendorfoe, decada=1):
    output = ""
    decada = int(decada)
    if decada == 1:
        top = 10
        low = 0
        toprange = "Top10"
    else:
        top = decada * 10
        topreal = top
        low = top - 9
        lowreal = low
        toprange = "Top" + str(low) + "-" + str(top)
    make_a_list = list(score_dict)[low:top]
    while make_a_list == [] and top >= 20:
        if top == 20:
            top = 10
            low = 0
        elif top > 20:
            top -= 10
        topreal = top
        lowreal = low
        if top == 10:
            toprange = "Top10"
        else:
            toprange = "Top" + str(low) + "-" + str(top)
        make_a_list = list(score_dict)[low:top]
    for i in make_a_list:
        if score_dict[i] != 0:
            output += inbold(scoreboard["real_nicks"][i]) + ": " + str(score_dict[i]) + " "
    return toprange + " " + friendorfoe[1:] + " : " + output

def sendmsg(connection, channel, msg):
    msg = split_msg(msg, 470)
    for i in range(len(msg)):
        joint = msg[i][0]
        connection.privmsg(channel, joint)

def remove_colors(message):
    regexc = re.compile(chr(3) + "(\d{,2}(,\d{,2})?)?", re.UNICODE)
    message = message.replace("\x1d", "")
    message = message.replace(r"\x31", "")
    message = message.replace("\x0f", "")
    message = message.replace(chr(29), "")
    message = message.replace(chr(2), "")
    message = regexc.sub("", message)
    return message

def save_scores():
    global scoreboard
    with open('duckhunt.pkl', 'wb') as fp:
        pickle.dump(scoreboard, fp)

def add_score(shooter, cmd, score):
    global scoreboard
    shooter = shooter.lower()
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
    player = player.lower()
    scoreboard["!bang"].pop(player)
    scoreboard["!bef"].pop(player)
    time.sleep(2)
    save_scores()

def load_scores():
    global scoreboard
    global DUCKLINES_TARGET
    global MISS_CHANCE
    if os.path.getsize('duckhunt.pkl') > 0:
        with open('duckhunt.pkl', 'rb') as fp:
            scoreboard = pickle.load(fp)
    if "real_nicks" not in scoreboard:
        scoreboard["real_nicks"] = {}
    if "ducklines" in scoreboard:
        DUCKLINES_TARGET = scoreboard["ducklines"]
    if "MISS_CHANCE" in scoreboard:
        MISS_CHANCE = scoreboard["MISS_CHANCE"]
    if "!bang" not in scoreboard:
        scoreboard["!bang"] = {}
    if "!bef" not in scoreboard:
        scoreboard["!bef"] = {}
    if "stats" not in scoreboard:
        scoreboard["stats"] = {}
    if "longest_duck" not in scoreboard["stats"]:
        scoreboard["stats"]["longest_duck"] = 0
    if "!bangmissed" not in scoreboard["stats"]:
        scoreboard["stats"]["!bangmissed"] = 0
    if "!befmissed" not in scoreboard["stats"]:
        scoreboard["stats"]["!befmissed"] = 0
    if "round_wins" not in scoreboard["stats"]:
        scoreboard["stats"]["round_wins"] = {}
    if "last_round_winner" not in scoreboard["stats"]:
        scoreboard["stats"]["last_round_winner"] = "N/A"
    if "streak" not in scoreboard["stats"]:
        scoreboard["stats"]["streak"] = 0
    if "longest_streak" not in scoreboard["stats"]:
        scoreboard["stats"]["longest_streak"] = 0
    if "longest_streak_holder" not in scoreboard["stats"]:
        scoreboard["stats"]["longest_streak_holder"] = "N/A"
    if "total_rounds" not in scoreboard["stats"]:
         scoreboard["stats"]["total_rounds"] = 0
    x = ["totalmissed", "!bangmissed", "!befmissed", "total!bang", "total!bef"]
    for i in x:
        if i not in scoreboard["stats"]:
            scoreboard["stats"][i] = 0
    save_scores()
    time.sleep(1)
    print("Scores loaded!")
    print(scoreboard)

def inbold(s):
    return "\x02" + s + "\x02"

def on_connectbot(connection, event):
    identify_cmd = ""
    print("Connection successfull")
    if NICKSERV_IDENTIFY == True:
        if NICKSERV_PASS != "":
            if NICKSERV_ACCOUNT != "":
                identify_cmd = "IDENTIFY %s %s" % (NICKSERV_ACCOUNT, NICKSERV_PASS)
            else:
                identify_cmd = "IDENTIFY %s" % NICKSERV_PASS
            connection.privmsg(NICKSERV_NAME, identify_cmd)
    time.sleep(2)
    connection.join(CHANNEL)

def on_nicknameinuse(connection, event):
    nick = connection.get_nickname()
    newnick = nick + "_"
    print(nick + " is in use. Retrying with " + newnick)
    connection.nick(newnick)

def on_join(connection, event):
    if connection.get_nickname() == event.source.nick:
        print("Joined", event.target)
        if event.target == CHANNEL:
            connection.privmsg(event.target, "The DuckHunt Begins!")

def fly_away(con):
    global theresaduck
    global ducktime
    global snipe_dir
    if theresaduck:
        theresaduck = 0
        ducktime = 0
    if snipe_dir:
        snipe_dir = 0
    con.privmsg(CHANNEL, "The duck flew away to another channel... ・゜゜・。 ​ 。・゜゜\_ø<​ FLAP flap ....lap")

def repost_duck(con, repost_time):
    global theresaduck
    if theresaduck == 0:
        return
    con.privmsg(CHANNEL, ">ø_/ 。・゜・゜゜・。・゜゜・。QUAAAACK QUAAACK!")
    thetimers.add_timer("repost_duck", int(repost_time), repost_duck, *(con, int(repost_time)))

def secs_to_dur(seconds):
    seconds = round(seconds)
    result = ""
    day = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    seconds = seconds
    if day > 0:
        result += str(day) + "d "
    if hour > 0:
        result += str(hour) + "h "
    if minutes > 0:
        result += str(minutes) + "m "
    if seconds > 0:
        result += str(seconds) + "s "
    return result

def unset_last_duck():
    global last_duck
    global last_duck_player
    last_duck = 0
    last_duck_player = ""

def on_pubmsg(connection, event):
    global theresaduck
    global ducklines
    global ducktime
    global DUCKLINES_TARGET
    global MISS_CHANCE
    global missed
    global snipe_dir
    global goggles_cooldown
    global last_duck
    global last_duck_player
    if len(remove_colors(event.arguments[0]).split()) == 0:
        return
    channel = event.target
    print(event.source.nick + ":", event.arguments[0])
    msg = remove_colors(event.arguments[0]).split()
    msg[0] = msg[0].lower()
    if theresaduck == 0 and snipe_dir == 0 and msg[0] not in ["!bang", "!bef", "!befriend", "!goggles", "!snipe", "!killers", "!friends", "!ducklines", "!ducks", "!allstats", "!misschance", "!duckdown"]:
        ducklines += 1
    if ducklines >= DUCKLINES_TARGET and theresaduck != 1:
        theresaduck = 1
        ducklines = 0
        ducktime = time.time()
        connection.privmsg(channel, "・゜゜・。 ​ 。・゜゜\_ø<​ FLAP F​LAP!")
        if FLYAWAY_TIME > 0:
            thetimers.add_timer("fly_away", FLYAWAY_TIME, fly_away, connection)
            thetimers.add_timer("repost_duck", int((FLYAWAY_TIME+10)/6), repost_duck, *(connection, int((FLYAWAY_TIME+10)/6)))
        else:
            thetimers.add_timer("repost_duck", 5, repost_duck, *(connection, 5))
        return
    if msg[0] == "!goggles":
        if snipe_dir:
            connection.privmsg(CHANNEL, "Type: " + "!snipe " + snipe_dir)
            return
        if theresaduck:
            connection.privmsg(CHANNEL, "What do you need the goggles for? There's a duck RIGHT HERE! ---> 。・゜゜\_ø<​ *QUAAAAACK QUACKQUACK*")
            return
        if "goggles" in cooldown and cooldown["goggles"] > 0:
            if cooldown["goggles"] == 1:
                cooldown["goggles"] += 1
                connection.privmsg(CHANNEL, "The goggles can only be used so often.. because... BECAUSE I SAID SO! HAH! wait a bit and use it again.")
            return
        cooldown["goggles"] = 1
        thetimers.add_timer("goggles_cooldown", 30, cooldown.pop, "goggles")
        givegoggles = random.randint(1,100)
        connection.privmsg(CHANNEL, "You look through the goggles, trying to locate a duck...")
        if givegoggles > 60:
            NORTH_SOUTH = ["N", "S"]
            dir = NORTH_SOUTH[random.randint(0,1)]
            WEST_EAST = ["W", "E"]
            dirtwo = WEST_EAST[random.randint(0,1)]
            true_dir = dir + dirtwo
            random_dist = random.randint(140,300)
            snipe_dir = true_dir + str(random_dist)
            time.sleep(2)
            connection.privmsg(CHANNEL, "...and you see a Duck... " + true_dir + " from here, " + str(random_dist) + "ft away! Type !snipe " + true_dir + str(random_dist))
            thetimers.add_timer("snipe_dir", 25, fly_away, connection)
        else:
            time.sleep(2)
            connection.privmsg(CHANNEL, "...but the fog is too thick, you can't see much...")
    if msg[0] == "!snipe":
        if snipe_dir == 0:
            if "snipe" in cooldown and cooldown["snipe"] > 0:
                if cooldown["snipe"] == 1:
                    cooldown["snipe"] += 1
                    if theresaduck:
                        connection.privmsg(CHANNEL, "Why are you trying to use the sniper for a duck right next to you?? Type !bang")
                    else:
                        connection.privmsg(CHANNEL, "Yeah.. waste sniper bullets for no reason! You need to look through the goggles first!!!")
            return
        cooldown["snipe"] = 1
        thetimers.add_timer("snipe", 30, cooldown.pop, "snipe")
        thetimers.cancel_timer("snipe_dir")
        if len(msg) > 1 and msg[1] == snipe_dir:
            old_snipe = snipe_dir
            snipe_dir = 0
            shooter = event.source.nick
            shooter_lower = shooter.lower()
            word = get_word("!bang")
            cmd = "!bang"
            add_score(shooter_lower, cmd, 1)
            score = scoreboard[cmd][shooter_lower]
            connection.privmsg(CHANNEL, "Congrats, " + shooter + "! You sniped the duck at " + old_snipe[0:1] + " and " + old_snipe[2:] + " ft away! You have "  + word["past"] + " " + str(score) + " ducks in " + channel + ".")
        else:
            snipe_dir = 0
            connection.privmsg(CHANNEL, "FAIL! You missed the duck and it got scared away!")
    if msg[0] == "!befriend":
        msg[0] = "!bef"
    bangbef = ["!bang", "!bef"]
    conds = [msg[0] == "!bang", msg[0] == "!bef"]
    shooter = event.source.nick
    shooter_lower = shooter.lower()
    if any(conds):
        scoreboard["real_nicks"][shooter_lower] = shooter
        cmd = bangbef[conds.index(True)]
        word = get_word(cmd)
        if theresaduck:
            if shooter_lower in missed:
                timemiss = round(time.time(), 0)
                timemissdiff = timemiss - missed[shooter_lower]
                if timemissdiff < 7:
                    return
            rand = random.randrange(1,100)
            if rand < MISS_CHANCE and shooter_lower not in missed:
                response = random_response(msg[0], shooter)
                connection.privmsg(channel, "MISS! " + response)
                missed[shooter_lower] = round(time.time(),0)
                scoreboard["stats"][cmd + "missed"] += 1
                scoreboard["stats"]["totalmissed"] += 1
                cmdshootermissed = cmd + shooter_lower + "missed"
                if not cmdshootermissed in scoreboard["stats"]:
                     scoreboard["stats"][cmdshootermissed] = 0
                scoreboard["stats"][cmdshootermissed] += 1
                save_scores()
                return
            timeshot = time.time()
            theresaduck = 0
            timediff = round(timeshot - ducktime, 3)
            saylongduck = ""
            if timediff > scoreboard["stats"]["longest_duck"]:
                record_diff = round(timediff - scoreboard["stats"]["longest_duck"], 0)
                saylongduck = "|| [New Record of Duck Freedom: " + secs_to_dur(round(timediff, 0)) + "Previous record: " + secs_to_dur(scoreboard["stats"]["longest_duck"])
                scoreboard["stats"]["longest_duck"] = timediff
            add_score(shooter_lower, cmd, 1)
            score = scoreboard[cmd][shooter_lower]
            missed = {}
            thetimers.cancel_timer("fly_away")
            thetimers.cancel_timer("repost_duck")
            last_duck = round(time.time(), 0)
            last_duck_player = shooter_lower
            thetimers.add_timer("unset_last_duck", 5, unset_last_duck)
            connection.privmsg(channel, "Congrats " + shooter + " you " + word["past"] + " the duck in " + str(timediff) + " seconds! You have " + word["past"] + " " + str(score) + " ducks in " +  channel + ". " + saylongduck)
            if score >= RESET_SCORE:
                scoreboard["stats"]["total_rounds"] += 1
                thetimers.add_timer("reset_score", 5, connection.privmsg, *(channel, "\o/ CONGRATS %s! You reached the winning score of %s CONGRATS \o/" % (shooter, RESET_SCORE)))
                thetimers.add_timer("celebrate", 6, connection.privmsg, *(channel, "CONGRATS %s CONGRATS! *.-.**!*;*:*;*!*?*!*;*;*;*!*;*;*:*:*;*;_-_-_*!*;*;*;?*!*!*;_-*+*+" % shooter))
                thetimers.add_timer("celebrate2", 8, connection.privmsg, *(channel, "CONGRATS %s CONGRATS! *.-.**!*;*:*;*!*?*!*;*;*;*!*;*;*:*:*;*;_-_-_*!*;*;*;?*!*!*;_-*+*+" % shooter))
                thetimers.add_timer("reset_score2", 20, connection.privmsg, *(channel, inbold("ALL SCORES, have been wiped and the DuckHunt begins new!")))
                scoreboard["!bef"] = {}
                scoreboard["!bang"] = {}
                if shooter_lower not in scoreboard["stats"]["round_wins"]:
                    scoreboard["stats"]["round_wins"][shooter_lower] = 0
                scoreboard["stats"]["round_wins"][shooter_lower] += 1
                if scoreboard["stats"]["last_round_winner"] == shooter_lower:
                    scoreboard["stats"]["streak"] += 1
                    if scoreboard["stats"]["streak"] > scoreboard["stats"]["longest_streak"]:
                        longest = scoreboard["stats"]["longest_streak"]
                        holder = scoreboard["stats"]["longest_streak_holder"]
                        if holder == shooter_lower:
                            isholder = shooter_lower
                        else:
                            isholder = holder
                        streakmsg = "%s BROKE the longest streak of %s consecutive round wins! Previously held by %s! Congrats!" % (shooter, longest, isholder)
                        thetimers.add_timer("streak_announce", 10, connection.privmsg, *(channel, streakmsg))
                        scoreboard["stats"]["longest_streak_holder"] = shooter_lower
                        scoreboard["stats"]["longest_streak"] += 1
                        save_scores()
                else:
                    if scoreboard["stats"]["streak"] > 1:
                        streak_diff = (scoreboard["stats"]["longest_streak"] - scoreboard["stats"]["streak"]) + 1
                        streakmsg = "%s BROKE %s's %s round streak! %s needed %s more wins to beat the longest streak held by %s" % (shooter, scoreboard["stats"]["last_round_winner"], scoreboard["stats"]["streak"], scoreboard["stats"]["last_round_winner"], streak_diff, scoreboard["stats"]["longest_streak_holder"])
                        thetimers.add_timer("streak_announce", 10, connection.privmsg, *(channel, streakmsg))
                    scoreboard["stats"]["streak"] = 1
                    scoreboard["stats"]["last_round_winner"] = shooter_lower
                    save_scores()
        else:
            if last_duck == 0:
                connection.privmsg(channel, "WTH " + shooter + "? There is no duck to " +  word["present"])
            else:
                if last_duck_player == shooter_lower:
                    return
                connection.privmsg(channel, "Sorry " + shooter + "! You missed by " +  str(round(time.time() - last_duck, 0)) + " Be faster next time!")
    if msg[0] == "!duckhelp":
        duckhelp = {"!bang": "Simply Shoots at the duck", "!bef": "Simply befriends the duck", "!goggles": "Lets you use the goggles for a chance to spot a duck in the distance", "!snipe": "Usage: !snipe <coords> | The coords parameter is random and is given by the duckbot after you find a distant duck with !goggles", "!duckstats": "Usage: !duckstats [user] | The user parameter is optional. If used, shows some game stats for user, if not used, stats of the sender", "!allduckstats": "Shows some general game stats", "!ducks": "Usage: !ducks [user] | Shows killed and friend ducks of [user] (if no user is given shows for sender", "!killers": "Usage: !killers N | N is an optional positive nunber, 1 shows the top 10 killers, 2 top11-20 etc", "!friends": "Usage: !friends  N | N is an optional positive nunber, 1 shows the top 10 friends, 2 top11-20 etc"}
        if len(msg) == 1:
            listcmds = []
            for i in duckhelp:
                listcmds.append(i)
            listcmds = " ".join(listcmds)
            connection.privmsg(channel, "Commands list: " + listcmds)
            time.sleep(1)
            connection.privmsg(channel, "!duckhelp <cmd> for specific command help.")
            return
        if msg[1] in duckhelp or "!" + msg[1] in duckhelp:
            msg[1] = "!" + msg[1].replace("!", "")
            connection.privmsg(channel, duckhelp[msg[1]])
        else:
            connection.privmsg(channel, "Invalid command. Do !duckhelp for a list of commands.")
    if msg[0] == "!allduckstats":
        scoreboard["real_nicks"][shooter_lower] = shooter
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
        statsline = inbold("Total rounds: ") + str(scoreboard["stats"]["total_rounds"]) + inbold(" Current streak: ") + str(scoreboard["stats"]["streak"]) + " by " +  scoreboard["stats"]["last_round_winner"] + inbold(" Longest Streak: ") + str(scoreboard["stats"]["longest_streak"] + 1) + " by " + scoreboard["stats"]["longest_streak_holder"] + inbold(" Successful shots: ") + str(scoreboard["stats"]["total!bang"]) + inbold(" Succesful friendships: ") + str(scoreboard["stats"]["total!bef"]) + inbold(" Missed shots: ") +  str(bangmissed) + inbold(" Missed friendships: ") + str(befmissed) + inbold(" Total missed: ") + str(totalmissed) + inbold(" Longest Duck Freedom: ") + str(scoreboard["stats"]["longest_duck"])
        connection.privmsg(channel, statsline)
    elif msg[0] == "!duckstats":
         scoreboard["real_nicks"][shooter_lower] = shooter
         stats = scoreboard["stats"]
         bang = scoreboard["!bang"]
         bef = scoreboard["!bef"]
         if len(msg) == 1:
             nick = event.source.nick.lower()
         else:
             nick = msg[1].lower()
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
        num = 1
        if len(msg) > 1 and msg[1].isnumeric() == True:
            num = msg[1]
        scoreboard["real_nicks"][shooter_lower] = shooter
        x = {k: v for k, v in sorted(scoreboard["!bang"].items(), key=lambda item: item[1], reverse=True)}
        the_scores = score_output(x, msg[0], num)
        sendmsg(connection, channel, the_scores)
        '''
        for p in x:
            if x[p] > 0:
                s += inbold(scoreboard["real_nicks"][p] + ": ") + str(x[p]) + " "
                counter += 1
                totalcounter += 1
                if (counter == 10 and len(x) >= 9) or totalcounter >= len(x):
                    counter = 0
                    themsg = "Killers in " + channel + ": " + s
                    sendmsg(connection, channel, themsg)
                    s = ""
       '''
    elif msg[0] == "!friends":
        num = 1
        if len(msg) > 1 and msg[1].isnumeric() == True:
            num = msg[1]
        scoreboard["real_nicks"][shooter_lower] = shooter
        x = {k: v for k, v in sorted(scoreboard["!bef"].items(), key=lambda item: item[1], reverse=True)}
        the_scores = score_output(x, msg[0], num)
        sendmsg(connection, channel, the_scores)
        '''
        for p in x:
            if x[p] > 0:
                s += inbold(scoreboard["real_nicks"][p] + ": ") + str(x[p]) + " "
        sendmsg(connection, channel, "Friends in " + channel + ": " + s)
        '''
    elif msg[0] == "!ducks":
        scoreboard["real_nicks"][shooter_lower] = shooter
        if len(msg) == 1:
            whoseducks = event.source.nick
            whoseducks_lower = whoseducks.lower()
            wordduck = ", you have"
        else:
            whoseducks = msg[1]
            whoseducks_lower = whoseducks.lower()
            wordduck = " has"
        if whoseducks_lower in scoreboard["!bang"]:
            killed = scoreboard["!bang"][whoseducks_lower]
            friended = scoreboard["!bef"][whoseducks_lower]
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
            nickmergefrom = msg[1].lower()
            nickmergeto = msg[2].lower()
            if nickmergefrom in scoreboard["!bang"]:
                scoreboard["real_nicks"][nickmergefrom] = msg[1]
                scoreboard["real_nicks"][nickmergeto] = msg[2]
                tomovebang = scoreboard["!bang"][nickmergefrom]
                add_score(nickmergeto, "!bang", tomovebang)
                tomovebef = scoreboard["!bef"][nickmergefrom]
                add_score(nickmergeto, "!bef", tomovebef)
                del_score(nickmergefrom)
                connection.privmsg(channel, "Moved " + str(tomovebang) + " dead ducks and " + str(tomovebef) + " befriended ducks from " + msg[1] + " to " + msg[2])
            else:
                connection.privmsg(channel, msg[1] + ": No such nick in my scoreboard.")
        elif msg[0] == "!misschance":
            if len(msg) == 1:
                connection.privmsg(channel, "Current Miss chance is: %s" % MISS_CHANCE)
                return
            if msg[1].isnumeric() == False or (msg[1].isnumeric() == True and int(msg[1]) not in range(1,101)):
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
        thetimers.check_timers()
        time.sleep(0.2)

startloop()

