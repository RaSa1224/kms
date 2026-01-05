from datetime import timedelta
import datetime
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
banwrds= ["nigger","nigga","naga","niga","ниггер","негр","нига","нигер","нага","faggot","пидор","пидорас","педик","гомик","хохол","аутист","даун","уёбище","zov","svo","чурка","daun","autist","churka","churca"]
join_role= "Unverified"
modroles= ["Main Leader","Hatsune Miku","Kasane Teto","☀️","☄️","⚡","💥","❄️","Staff Admin","Administrator","Curator","Master","Отвечает за Moderator","Moderator","Отвечает за Support","Support","Отвечает за Tribunemod","Tribunemod","Отвечает за Closemod","Closemod","Отвечает за Eventsmod","Eventsmod","Отвечает за Creative","Creative","Отвечает за Creative","Creative","Отвечает за Staff","Staff"]
load_dotenv()
token= os.getenv('DISCORD_TOKEN')

handler= logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents= discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f"It's working, {bot.user.name}")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=join_role)
    if role:
        await member.add_roles(role)

    await member.send(f"Добро пожаловать на сервер {member.name}!")

@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word in message.content.lower() for word in banwrds):
        await message.delete()  
        await message.channel.send(f"{message.author.mention} Без запреток пжпж")

    await bot.process_commands(message)

@bot.command()
@commands.has_any_role(*modroles)
async def poll(ctx, *, question):
    embed = discord.Embed(title="Новый опрос", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
@poll.error
async def poll_errror(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("У вас нету роли способной на данное действие")

@bot.command()
async def roll(message):
    rolled_num= random.randint(1,6)
    await message.channel.send(f"{message.author.mention} вам выпало {rolled_num}🎲!")

MESSAGE_ID = 1445806578581241940
ROLE_ID = 1445795881923121304
EMOJI = "✅"

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID:
        return

    if str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(ROLE_ID)
    member = guild.get_member(payload.user_id)

    if member is not None:
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != MESSAGE_ID:
        return

    if str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(ROLE_ID)
    member = guild.get_member(payload.user_id)

    if member is not None:
        await member.remove_roles(role)
    

@bot.command()
@commands.has_any_role(*modroles)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="Без причины"):
    until = discord.utils.utcnow() + discord.timedelta(minutes=minutes)

    try:
        await member.timeout(until, reason=reason)

        await ctx.send(
            f"🔇 {member.mention} получил таймаут на **{minutes} мин.**\n"
            f"📄 Причина: *{reason}*"
        )

    except discord.Forbidden:
        await ctx.send("❌ У бота нет прав для выдачи тайм-аутов!")

    except Exception as e:
        await ctx.send(f"❌ Ошибка: {e}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: int, *, reason="Причина не указана"):
    try:
        until = discord.utils.utcnow() + datetime.timedelta(minutes=time)
        await member.timeout(until, reason=reason)

        await ctx.send(f"🔇Пользователь {member.mention} замучен на {time} минут.\nПричина: {reason}")

    except Exception as e:
        await ctx.send("❌Не удалось выдать мут.")
        print(e)

#команда для размута
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"✅Пользователь {member.mention} размучен.")

    except:
        await ctx.send("❌Не удалось снять мут.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
