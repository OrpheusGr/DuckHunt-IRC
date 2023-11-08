SERVER = "irc.some.net"
PORT = 6667 # no quotes on this
NICK = "DuckHunt" # or whatever you want
CHANNEL = "#channelhere"
NICKSERV_IDENTIFY = False # False or True
NICKSERV_NAME = "NickServ" # most of the time NickServ
NICKSERV_ACCOUNT = "" # if you wanna identify as a specific account other than the bot's nick
NICKSERV_PASS = "" # your password here
DUCKLINES_TARGET = 5 # you can change this on IRC with !ducklines command and the bot will save it and load it whenever it's started
#also no quotes ^
duckops = ["input_a_nick_here", "and_another_here", "and_so_on", "or_just_put_a_single_one_without_commas"] # these nicks will be able to use !merge from_nick to_nick
MISS_CHANCE = 35 # you can also change this on IRC with !misschance command and that value will be saved and used instead of this
#also no quotes^
FLYAWAY_TIME = 0 # 0 for no fly away, any other numerical value for the duck to fly after not been shot for

