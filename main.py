import discord
import os
from keep_alive import keep_alive
from discord.ext import commands

# from replit import db
# db["key"] = "value"
# value = db["key"]
# del db["key"]
# keys = db.keys()
# matches = db.prefix("prefix")
# db["number"] = {
#     "counter": 1,
# }
# print(db["number"])
import sqlite3
conn = sqlite3.connect("deezgunz.db") # db - database
cursor = conn.cursor()
create_table = """
CREATE TABLE deezgunz (
   userid varchar(18) NOT NULL,
   thread INT DEFAULT 0
);
"""
# cursor.execute(create_table)
conn.commit()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=',', intents=intents)

@bot.event
async def on_ready():
  print("I'm in")
  print(bot.user)
  await bot.change_presence(activity=discord.Game(",help | Assisting You!"))

@bot.event
async def on_message(message):
  if not message.author.bot and message.author != bot.user and not message.guild:
    #Make user
    cursor.execute('Select * from deezgunz where userid = ?', (message.author.id,))
    rows1 = cursor.fetchall()
    if(rows1 == []):
      cursor.execute('insert into deezgunz(userid, thread) values(?,?)', (message.author.id,1,))
    else:
      cursor.execute('Select * from deezgunz where userid = ?', (message.author.id,))
      rows1 = cursor.fetchall()
      conn.commit()
    # Mod mail
    cursor.execute('Select * from deezgunz where userid = ?', (message.author.id,))
    rows1 = cursor.fetchall()
    if rows1[0][1] == 0:
      cursor.execute('update deezgunz set thread = ? where userid = ?', (1)),
      server = bot.get_guild(763913144653316126)
      channel = server.get_channel(842464175472115754)
      await channel.send(f'({message.author.id}){message.author}  has said {message}')
      server_add = discord.Embed(title="Support", color=discord.Color.green())
      server_add.add_field(name=f'New Thread',
                        value=f'The staff will get back to you as soon as possible, please bare with us!\n \n Thanks,\nSoftwaresat Bot Staff Team',
                        inline=True)
      await message.author.send(embed=server_add)
      await channel.send(embed=server_add)
    elif rows1[0][1] == 1:
      user = bot.get_user(420339994754940928)
      # await user.send('👀')
      guild = bot.get_guild(763913144653316126)
      # member = await message.guild.fetch_member(message.author.id)
      await message.author.send(f'Please chat in Softwaresat Community! {rows1[0][1]}')

  await bot.process_commands(message)

#Suggestions!
@bot.command()
async def suggest(message, *, suggestion: str):
  """Suggest a wonderful idea!"""
  guild = message.guild
  channel = guild.get_channel(805963952059318283)
  suggestion_embed = discord.Embed(title='Suggestion!', description=f'Suggestion Made By: **{message.author}**', color=discord.Color.green())
  suggestion_embed.set_thumbnail(url=message.author.avatar_url)
  suggestion_embed.add_field(name='My Suggestion is:',
                    value=suggestion,
                    inline=True)
  msg = await channel.send(embed=suggestion_embed)
  await message.channel.send("Your suggestion has been sent successfully!")
  await msg.add_reaction('\U0001f44d')
  await msg.add_reaction('\U0001f44e')

#reply!
@bot.command()
@commands.has_permissions(administrator=True)
async def mod_reply(message, id: int, *, reply: str):
  """Reply to Mod Mail - Admin Only!"""
  member = await message.guild.fetch_member(id)
  try: 
    suggestion_embed = discord.Embed(title='Staff Reply!', description=f'Reply Made By: **{message.author}**', color=discord.Color.gold())
    suggestion_embed.set_thumbnail(url=message.author.avatar_url)
    suggestion_embed.add_field(name='Reply:',
                      value=f'{reply}',
                      inline=True)
    await member.send(embed=suggestion_embed)
    await message.channel.send(embed=suggestion_embed)
  except:
    await message.channel.send('This message cannot be send. A possible cause is that this server may not have my owner in it! Go to my support server for help.')

#Approve!
@bot.command()
@commands.has_permissions(administrator=True)
async def approve(message, message_id: int, *, notes: str):
  """Administrator Only - Approve Suggestions"""
  guild = message.guild
  channel = guild.get_channel(805963952059318283)
  msg = await channel.fetch_message(message_id)
  suggestion = discord.Embed(title='Suggestion **approved**!', description=f'Suggestion approved by: **{message.author}**', color=discord.Color.green())
  suggestion.add_field(name='Notes:',
                    value=notes,
                    inline=True)
  await msg.reply(embed=suggestion)
  await message.channel.send(f'Suggestion **approved** by **{message.author}**!')

#serverinfo Command
@bot.command()
async def serverinfo(message):
    """Get your server's info!"""
    server = message.guild
    num_categories = len(server.categories)
    icon = server.icon_url
    member_count = server.member_count
    created_at = server.created_at
    num_emoji = len(server.emojis)
    id = server.id
    owner = server.owner
    name = server.name
    description = server.description
    num_c = len(server.channels)
    num_vc = len(server.voice_channels)
    num_tc = len(server.text_channels)
    boost_level = server.premium_tier
    total_boosts = server.premium_subscription_count
    role_count = len(server.roles)
        
    
    embedVar = discord.Embed(title=f'Info for {name}!', description=f'Description for server: {description}', color=discord.Color.blue())
    embedVar.set_thumbnail(url=icon) 
    embedVar.add_field(name="ID", value=id, inline=True)
    embedVar.add_field(name="Owner", value=owner, inline=True)
    embedVar.add_field(name="Created at", value=created_at, inline=True)
    embedVar.add_field(name="Member Count", value=f'Total Members: {member_count}', inline=True)
    embedVar.add_field(name="Channel/Category Info", value=f'Total Categories: {num_categories}\nTotal Channels: {num_c}\nText Channels: {num_tc}\nVoice Channels: {num_vc}', inline=True)
    embedVar.add_field(name="Boost Info", value=f'Boost Level: {boost_level}\nTotal Boosts: {total_boosts}', inline=True)
    embedVar.add_field(name="Role/Emoji Info", value=f'Number of Roles: {role_count}\nNumber of Emojis: {num_emoji}', inline=True)
    embedVar.set_footer(text=f'Requested by {message.author}!')
    await message.channel.send(embed=embedVar)

#Deny!
@bot.command()
@commands.has_permissions(administrator=True)
async def deny(message, message_id: int, *, notes: str):
  """Administrator Only - Deny Suggestions"""
  guild = message.guild
  channel = guild.get_channel(805963952059318283)
  msg = await channel.fetch_message(message_id)
  suggestion = discord.Embed(title='Suggestion **denied**!', description=f'Suggestion denied by: **{message.author}**', color=discord.Color.red())
  suggestion.add_field(name='Notes:',
                    value=notes,
                    inline=True)
  await msg.reply(embed=suggestion)
  await message.channel.send(f'Suggestion has been **denied** by **{message.author}**!')

#oneword story
@bot.command()
async def story(message):
    """Read the story!"""
    f = open("story.txt", "r")
    await message.send(file=discord.File('story.txt'))
    f.close()

# #oneword story add
# @bot.command()
# async def add(ctx, *, word: str):
#     """Add words to the story!!"""
#     f = open("story.txt", "a")
#     if word == "":
#         await ctx.channel.send('Please add a word or a set of words!')
#     f.write(str(f' {word}'))
#     await ctx.channel.send("I have successfully added the words!")
#     f.close()

@suggest.error
async def suggest_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArguments):
    await ctx.send("Please make sure your syntax is correct! Ex: `$suggest This is my suggestion`")

@approve.error
async def approve_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArguments):
    await ctx.send("Please make sure your syntax is correct! Ex: `$approve 830224912476143678 Great Suggestion!`")
@deny.error
async def deny_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArguments):
    await ctx.send("Please make sure your syntax is correct! Ex: `$deny 830224912476143678 I don't think this is a good idea!")
@deny.error
async def admin1_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You need Administrator Permissions to run this!")
@approve.error
async def admin2_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You need Administrator Permissions to run this!")

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
