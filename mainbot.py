import discord
from discord.ext import commands
from discord.utils import get
import random
import youtube_dl
import os
import time
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess



# serverid = 327481954427731969

def read_token():
    with open('txt\Token.txt', "r") as file:
        lines = file.readlines()
        return lines[0].strip()


token = read_token()

client = commands.Bot(command_prefix=".")


async def is_allowed(ctx):
    allowed = False
    if ctx.author.id == 426103778026979328:
        allowed = True
    if ctx.author.id == 308430209705836556:
        allowed = True
    return allowed


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Flirting with MEG PIT"))
    print("bot has connected to Discord")
    client.load_extension('cogs.music')


@client.event
async def on_member_join(member):
    id = client.get_guild(327481954427731969)

    print(f"""{member} has joined server""")



@client.event
async def on_member_remove(member):
    print(f"""{member} has left the server""")


@client.command()
async def Help(ctx):
    embed = discord.Embed(title="List of Commands", description="Start every command with the \".\" key")

    # insult
    embed.add_field(name="insult (i)",
                    value="A quick and easy way to insult anyone, just add their name at the end of the command",
                    inline=False)

    # clear
    embed.add_field(name="clear (c)",
                    value="Clears one message by default, but takes parameter to delete up to 125 messages",
                    inline=False)

    # join
    embed.add_field(name="join (j)",
                    value="Forces bot to join your voice channel",
                    inline=False)

    # leave
    embed.add_field(name="leave (l)",
                    value="Forces bot to leave your voice channel",
                    inline=False)

    # play
    embed.add_field(name="play (p)",
                    value="Use this command with a youtube URL to play any audio from youtube",
                    inline=False)

    # MLG
    embed.add_field(name="MLG_AIRHORN (mlg)",
                    value="Plays mlg airhorns",
                    inline=False)

    # GSO
    embed.add_field(name="Nolans_Message (gso)",
                    value="Plays Nolan's special message",
                    inline=False)

    await ctx.channel.send(embed=embed)


@client.command()
async def AHelp(ctx):
    embed = discord.Embed(title="List of Commands for Admins", description="Start every command with the \".\" key")

    # insult
    embed.add_field(name="kick",
                    value="Used to kick somone from the server, follow the kick command with the @ of the person "
                          "being kicked along with the reason for why they are being kicked",
                    inline=False)

    await ctx.channel.send(embed=embed)


@client.command(aliases=["i"])
async def insult(ctx, *, name):
    bad_names = ["connor", "Connor", "konnor", "Konnor", "conner", "Conner", "konner", "Konner"]
    if name in bad_names:
        name = "Brian"
    await ctx.send(f"""{name} {randInsult()}""")


def randInsult():
    s = open("txt\Insults.txt", "r")
    m = s.readlines()
    l = []
    for i in range(0, len(m) - 1):
        x = m[i]
        z = len(x)
        a = x[:z - 1]
        l.append(a)
    l.append(m[i + 1])
    o = random.choice(l)
    s.close()
    return o


@client.command()
async def ping(ctx):
    await ctx.send(f"""{client.latency * 1000} ms""")


@client.command(aliases=["c"])
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.check(is_allowed)
async def kick(ctx, memeber: discord.Member, *, reason=None):
    await memeber.kick(reason=reason)
    print(f"""Member {memeber} was kicked for {reason}""")


@client.command(aliases=["ccn"])
@commands.check(is_allowed)
async def editChannelName(ctx, channel: discord.VoiceChannel, *, new_name):
    await channel.edit(name=new_name)

@client.command(aliases=["cn"])
@commands.check(is_allowed)
async def editUserName(ctx, member: discord.Member, *, new_name):
    await member.edit(nick=new_name)


@client.command(aliases=["kd"])
async def findKD(ctx, console, gamertag):

    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(PATH)

    driver.get("https://cod.tracker.gg/")

    print(f"Driver connected to {driver.title}")

    consoleDropDown = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div/main/div[2]/div[1]/div/div/div[1]/div[2]/div/div[2]')

    consoleDropDown.click()

    xbox = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div/main/div[2]/div[1]/div/div/div[1]/div[2]/div/div[2]/ul/li[4]')
    playstation = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div/main/div[2]/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/ul/li[1]')

    if console == 'xbox':
        xbox.click()

    elif console == 'ps4':
        playstation.click()

    search = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div/main/div[2]/div[1]/div/div/div[1]/div[2]/form/input')

    search.send_keys(gamertag)
    search.send_keys(Keys.ENTER)

    time.sleep(3)

    try:
        kd = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[2]/div/main/div[2]/div[3]/div[2]/div/div/div[1]/div[3]/div[1]/div/div[2]/span[2]')
        await ctx.send(f"{gamertag} has a K/D of {kd.text}")
        driver.close()
    except Exception as e:
        await ctx.send("USER NOT FOUND")
        driver.close()



# VOICE COMMANDS

@client.command()
async def joinc(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()



@client.command(aliases=["mlg"])
async def MLG_AIRHORN(ctx):
    await joinc(ctx)
    time.sleep(1)
    voic = get(client.voice_clients, guild=ctx.guild)
    voic.play(discord.FFmpegPCMAudio("audio\MLG Horns.mp3"))
    voic.source = discord.PCMVolumeTransformer(voic.source)
    voic.source.volume = 0.3
    time.sleep(4)
    await leave(ctx)


@client.command(aliases=["gso"])
async def Nolans_message(ctx):
    await joinc(ctx)
    time.sleep(1)
    voic = get(client.voice_clients, guild=ctx.guild)
    voic.play(discord.FFmpegPCMAudio("audio\Nolans Message.mp3"))
    voic.source = discord.PCMVolumeTransformer(voic.source)
    voic.source.volume = 0.3
    time.sleep(4)
    await leave(ctx)


@client.command(aliases=["tscott", "il"])
async def ITSLIT(ctx):
    await joinc(ctx)
    time.sleep(1)
    voic = get(client.voice_clients, guild=ctx.guild)
    voic.play(discord.FFmpegPCMAudio("audio\ITSLIT.mp3"))
    voic.source = discord.PCMVolumeTransformer(voic.source)
    voic.source.volume = 0.3
    time.sleep(4)
    await leave(ctx)


client.run(token)
