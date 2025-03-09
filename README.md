# DuckHunt-IRC
A simple DuckHunt IRC bot, simular to Gonzobot's but coded from scratch, with more features like rounds and stats.

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
  - !allduckstats (shows general game stats)
  - !duckstats [nick] (With a parameter it shows stats for nick, without it shows stats for the sender)
  - !ducks (shows how many ducks you killed and befriended)
  - !goggles (60% chance of locating a duck in the distance)
  - !snipe (using the directions from !goggles the player can snipe the located duck)
  - !killers N
  - !friends N
    - N is optional - Can be a positive number. No N or 1 shows top10, 2 shows 11-20 etc etc
  - !duckhelp cmd - Example: !duckhelp !killers shows help for !killers - If no command is given, shows list of commands.
- Duckops commands (In private messages)
  - !merge somenick someothernick (Moves somenick's ducks to someothernick's ducks
  - !ducklines N  (sets the amount of lines a duck will spawn at to N lines. If no parameter is sent, it shows the current setting)
  - !misschance 0-100 (sets the chance of missing a shot or a.. befriending)
  - !duckdown (kills the bot)

- Extra feats
  - NickServ identification
  - You can have the duck fly away after a period of time you choose
  - Find a duck in the distance with !goggles and !snipe it 
  - The duck will requack when it's hasn't been shoot
  - Set a score target at which the round ends, stats remain but scores are wiped, starting the game from scratch.
