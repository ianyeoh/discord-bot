# discord-bot
A custom Discord bot written in Python 3.8. Implements commands that automate some repetitive tasks.

## Commands  
All commands must be prefixed with '$'.  

### test
```
  Usage: $test
```
- Command to test the bot is working. The bot should reply with: 'Hello!'.  

### kickmeafter
```
  Usage: $kickmeafter [time] [units: secs/mins/hrs]
```
- Once called, the bot will kick the calling user from their currently joined voice channel after specified delay.

### purge
```
  Usage: $purge
```
- Kicks all members in the discord that haven't been assigned the 'purge immune' role.
- Useful for Discord servers that have a large amount of users that join and leave.
