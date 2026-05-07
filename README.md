# Discord Staff Bot 👥

A Discord bot that tracks staff members' online status and duty time.

## Features

✅ **Staff Online Status** - See who's currently online/offline  
✅ **Duty Time Tracking** - Automatic tracking of how long staff are online  
✅ **Leaderboard** - View staff ranked by total duty time  
✅ **Session History** - Track individual work sessions  
✅ **Easy Commands** - Simple slash commands to check status and stats  

## Requirements

- Python 3.8+
- Discord.py 2.3+
- A Discord server with a "Staff" role

## Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/marjangagon/discord-staff-bot.git
   cd discord-staff-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your bot token**
   - Open `config.py`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual Discord bot token
   - Get a token from [Discord Developer Portal](https://discord.com/developers/applications)

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" and click "Add Bot"
4. Under TOKEN, click "Copy" and paste it in `config.py`
5. Enable these **Intents**:
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 → URL Generator
7. Select scopes: `bot`
8. Select permissions: `Read Messages/View Channels`, `Send Messages`, `Embed Links`
9. Copy the generated URL and invite the bot to your server

## Commands

### `!staffstatus`
Shows all staff members and their online/offline status with total duty time.

**Example:**
```
!staffstatus
```

### `!dutytime [@member]`
Check total duty time for a staff member (yourself if no member specified).

**Example:**
```
!dutytime @JohnDoe
!dutytime  # Check your own duty time
```

### `!staffleaderboard`
Display a leaderboard of staff ranked by total duty time.

**Example:**
```
!staffleaderboard
```

### `!resetstaffdata` (Admin only)
Reset all staff duty time data.

**Example:**
```
!resetstaffdata
```

## Setup Requirements

1. **Create a "Staff" role** in your Discord server
2. **Assign the role** to staff members you want to track
3. The bot will automatically start tracking when they go online/offline

## Data Storage

Staff data is stored in `staff_data.json` and includes:
- Total duty time (in minutes)
- Session history with start/end times
- Duration of each session

## Configuration

Edit `config.py` to customize:
- `TOKEN` - Your Discord bot token
- `BOT_PREFIX` - Command prefix (default: `!`)
- `STAFF_ROLE_NAME` - Name of the staff role to track

## Troubleshooting

**Bot not responding?**
- Check if bot token is correct in `config.py`
- Ensure bot has permissions in the channel
- Check if bot is running (`python bot.py`)

**Staff data not tracking?**
- Make sure staff members have the "Staff" role
- Check bot has "View Members" permission
- Restart the bot

**Commands not working?**
- Prefix your commands with `!` (e.g., `!staffstatus`)
- Ensure bot has "Send Messages" and "Embed Links" permissions

## Future Features

- 📊 Detailed analytics and charts
- 🔔 Notifications when staff go online/offline
- 📅 Weekly/monthly reports
- 🎯 Duty time goals and achievements
- 💾 Database integration (SQLite/PostgreSQL)

## License

MIT License - Feel free to modify and use!

## Support

For issues or feature requests, open an issue on GitHub.

---

**Happy tracking!** 🚀
