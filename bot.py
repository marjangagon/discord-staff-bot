import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, timedelta

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Data file for tracking staff duty times
STAFF_DATA_FILE = "staff_data.json"

def load_staff_data():
    """Load staff data from JSON file"""
    if os.path.exists(STAFF_DATA_FILE):
        with open(STAFF_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_staff_data(data):
    """Save staff data to JSON file"""
    with open(STAFF_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('------')
    check_staff_status.start()

@tasks.loop(minutes=1)
async def check_staff_status():
    """Periodically check and update staff status"""
    staff_data = load_staff_data()
    
    for guild in bot.guilds:
        # Get the staff role (you can customize this)
        staff_role = discord.utils.get(guild.roles, name="Staff")
        
        if not staff_role:
            continue
        
        for member in guild.members:
            if staff_role in member.roles:
                member_id = str(member.id)
                
                if member_id not in staff_data:
                    staff_data[member_id] = {
                        "name": member.name,
                        "duty_time_minutes": 0,
                        "sessions": []
                    }
                
                # Check if member is online
                if member.status != discord.Status.offline:
                    # Update or create current session
                    if "current_session_start" not in staff_data[member_id]:
                        staff_data[member_id]["current_session_start"] = datetime.now().isoformat()
                else:
                    # Member went offline, save session
                    if "current_session_start" in staff_data[member_id]:
                        start = datetime.fromisoformat(staff_data[member_id]["current_session_start"])
                        end = datetime.now()
                        duration = int((end - start).total_seconds() / 60)
                        
                        staff_data[member_id]["sessions"].append({
                            "start": staff_data[member_id]["current_session_start"],
                            "end": end.isoformat(),
                            "duration_minutes": duration
                        })
                        
                        staff_data[member_id]["duty_time_minutes"] += duration
                        del staff_data[member_id]["current_session_start"]
    
    save_staff_data(staff_data)

@bot.command(name='staffstatus', help='Check current staff online status')
async def staff_status(ctx):
    """Display current staff online status"""
    staff_data = load_staff_data()
    
    staff_role = discord.utils.get(ctx.guild.roles, name="Staff")
    
    if not staff_role:
        await ctx.send("❌ Staff role not found. Make sure there's a role called 'Staff'")
        return
    
    embed = discord.Embed(
        title="👥 Staff Status",
        description="Current staff members online/offline",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    online_staff = []
    offline_staff = []
    
    for member in ctx.guild.members:
        if staff_role in member.roles:
            member_id = str(member.id)
            duty_time = staff_data.get(member_id, {}).get("duty_time_minutes", 0)
            
            if member.status != discord.Status.offline:
                online_staff.append((member.name, duty_time))
            else:
                offline_staff.append((member.name, duty_time))
    
    if online_staff:
        online_list = "\n".join([f"🟢 {name} - {duty_time//60}h {duty_time%60}m" for name, duty_time in online_staff])
        embed.add_field(name="Online", value=online_list, inline=False)
    
    if offline_staff:
        offline_list = "\n".join([f"⚫ {name} - {duty_time//60}h {duty_time%60}m" for name, duty_time in offline_staff])
        embed.add_field(name="Offline", value=offline_list, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='dutytime', help='Check total duty time for a staff member')
async def duty_time(ctx, member: discord.Member = None):
    """Check total duty time for a specific staff member"""
    if member is None:
        member = ctx.author
    
    staff_data = load_staff_data()
    member_id = str(member.id)
    
    if member_id not in staff_data:
        await ctx.send(f"❌ No duty time data for {member.mention}")
        return
    
    data = staff_data[member_id]
    total_minutes = data.get("duty_time_minutes", 0)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    embed = discord.Embed(
        title=f"⏱️ Duty Time - {member.name}",
        description=f"Total duty time: **{hours}h {minutes}m**",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )
    
    sessions = data.get("sessions", [])
    if sessions:
        embed.add_field(name=f"Total Sessions", value=f"{len(sessions)}", inline=True)
        # Show last 5 sessions
        recent_sessions = sessions[-5:]
        session_list = "\n".join([
            f"📌 {s['duration_minutes']} min" 
            for s in recent_sessions
        ])
        embed.add_field(name="Recent Sessions", value=session_list, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='staffleaderboard', help='Show staff duty time leaderboard')
async def staff_leaderboard(ctx):
    """Display staff duty time leaderboard"""
    staff_data = load_staff_data()
    staff_role = discord.utils.get(ctx.guild.roles, name="Staff")
    
    if not staff_role:
        await ctx.send("❌ Staff role not found.")
        return
    
    # Create leaderboard
    leaderboard = []
    for member in ctx.guild.members:
        if staff_role in member.roles:
            member_id = str(member.id)
            duty_time = staff_data.get(member_id, {}).get("duty_time_minutes", 0)
            leaderboard.append((member.name, duty_time))
    
    # Sort by duty time (descending)
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    
    embed = discord.Embed(
        title="🏆 Staff Duty Time Leaderboard",
        color=discord.Color.gold(),
        timestamp=datetime.now()
    )
    
    leaderboard_text = ""
    for idx, (name, duty_time) in enumerate(leaderboard, 1):
        hours = duty_time // 60
        minutes = duty_time % 60
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        leaderboard_text += f"{medal} {name} - {hours}h {minutes}m\n"
    
    embed.description = leaderboard_text if leaderboard_text else "No staff data available"
    await ctx.send(embed=embed)

@bot.command(name='resetstaffdata', help='Reset all staff duty time data (Admin only)')
async def reset_staff_data(ctx):
    """Reset all staff data (requires admin)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ You need administrator permissions to use this command.")
        return
    
    save_staff_data({})
    await ctx.send("✅ All staff duty time data has been reset.")

# Run the bot
if __name__ == "__main__":
    from config import TOKEN
    bot.run(TOKEN)
