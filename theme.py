# In this file you can change the "theme" of the game
# If you want it to be something else from ducks you can change "duck"  "ducks"
# to "swans" or anything you might desire, you can also add an alias for !bang and !befriend
# Pretty much the entirety of the bot's language can be modified to your needs


# Below you can change the animal/object that is being hunted
# make sure not to delete the quotes

ALIAS_DUCK = "Duck"
ALIAS_DUCKS = "Duck"

# Below you may add an alias command for !bang

ALIAS_BANG = "!bang"

# Below you can do the same for !befriend

ALIAS_BEF = "!bef"

# Below you can change the "FLAP FLAP.. etc msg that is sent when a duck spawns. You can use a list and the bot will select a random one each time
## example below:
## ALIAS_FLAP = ["A wild duck spawns", "A wild swan appears", "A black hawk flies"]

ALIAS_FLAP = [
    "・゜゜・。 ​ 。・゜゜_ø<​ FLAP F​LAP!",
    "・゜゜・。 ​ 。・゜゜・゜゜・。_ø<​ FLAP F​LAP!"
]

ALIAS_REPOST = "・゜゜・。 ​ 。・゜゜_ø<​ FLAP F​LAP!"

# Below you can change how the bot refers to the action of whatever you changed the commands to
# e.g for !bang it was "you shot a duck" or "shoot the duck now"
# You will set a word for present and past tense

ALIAS_BANG_WORD_PRESENT = "shoot"
ALIAS_BANG_WORD_PAST = "shot"

ALIAS_BEF_WORD_PRESENT = "befriend"
ALIAS_BEF_WORD_PAST = "befriended"

# Below you can change several commands like !duckstats !allduckstats etc

ALIAS_DUCKSTATS = "!duckstats"
ALIAS_ALLDUCKSTATS = "!allduckstats"

ALIAS_GOGGLES = "!goggles"

ALIAS_GOGGLES_WORD = "goggles"

# Below you can change the responses of the bot when someone uses !goggles or its alias that you set above
# Note: This changes the entire message and not just replace some words in it

ALIAS_GOGGLES_ATTEMPT_REPLY = "You look through the goggles trying to locate a duck"

ALIAS_GOGGLES_FAIL_REPLY = "The fog is too thick you can't see much"

# in the below message use %s where the "Type !snipe or !dart etc message should go and %s will be replaced by the bot

ALIAS_GOGGLES_SUCCESS_REPLY = "And you manage to find a duck!"

# below type whatever should be said when a duck flies away (or in other terms  whatever your object is despawns, if you have flying away enabled)

ALIAS_FLY_AWAY_MSG = "The duck flew away"

# Below you can change how the bot refers to players that use either command
ALIAS_KILLERS = "killers"
ALIAS_FRIENDS = "friends"

# Below you can change how the bot refers to stats in the stat messages replies

ALIAS_SHOTS = "shots"
ALIAS_FRIENDSHIPS = "befriendings"

# And an alias for !killers and !friends:

ALIAS_CMD_KILLERS = "!killers"
ALIAS_CMD_FRIENDS = "!friends"
# In addition to this theme feature you can change the lines in responses.txt
# To match your choice of theme

# Please do not change anything below this line :)

def get_word(cmd):
    if cmd == "!bang":
        return {"present": ALIAS_BANG_WORD_PRESENT, "past": ALIAS_BANG_WORD_PAST}
    else:
        return {"present": ALIAS_BEF_WORD_PRESENT, "past": ALIAS_BEF_WORD_PAST}
