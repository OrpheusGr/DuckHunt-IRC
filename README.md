# DuckHunt-IRC
A simple DuckHunt IRC bot, simular to Gonzobot's but coded from scratch.

# Dependencies
Install (irc)[https://pypi.org/project/irc/]

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

- Duckops commands
  - !merge somenick someothernick (Moves somenick's ducks to someothernick's ducks
  - !ducklines 483 (sets the amount of lines a duck will spawn at. If no parameter is sent, it shows the current setting)
  - !misschance 0-100 (sets the chance of missing a shot or a.. befriending)

