# DuckHunt-IRC
A simple DuckHunt IRC bot, simular to Gonzobot's but coded from scratch.

# Dependencies
 * Python3.7 or above (probably)
 * Install [irc](https://pypi.org/project/irc/)

# Set up and running

- Make a copy of examplesettings.py named settings.py
- Fill out the values in settings.py
- Run the bot with ```python3 duckhunt.py```

# IRC commands

- Public commands
  - !bang (shoot the duck)
  - !bef (make friends with the duck)
  - !allstats (shows general game stats)
  - !stats [nick] (With a parameter it shows stats for nick, without it shows stats for the sender)
  - !ducks (shows how many ducks you killed and befriended)
  - !goggles (60% chance of locating a duck in the distance)
  - !snipe (using the directions from !goggles the player can snipe the located duck)

- Duckops commands
  - !merge somenick someothernick (Moves somenick's ducks to someothernick's ducks
  - !ducklines N  (sets the amount of lines a duck will spawn at to N lines. If no parameter is sent, it shows the current setting)
  - !misschance 0-100 (sets the chance of missing a shot or a.. befriending)
  - !duckdown (kills the bot)

- Extra feats
  - NickServ identification
  - You can have the duck fly away after a period of time you choose
  - Find a duck in the distance with !goggles and !snipe it 
  - The duck will requack when it's hasn't been shoot
