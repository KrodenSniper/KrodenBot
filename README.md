# KrodenBot
Discord Bot for ContinuumFall

This will rename voice channels to the most common game everybody in the channel is playing, as well as auto-add game-specific roles to members whenever they run a game.  The game name -> role name mapping is defined in the config.json, as well as the default voice channel names for when nobody is in the channel.

# Installation
This requires Python 3 be installed (tested with 3.7.3).  

This also requires the discord package:

Run: python -m pip install discord

# Configuration
See included config.json file.

You will need to modify the file and add your own token at the top.

# Running
Run: python main.py

