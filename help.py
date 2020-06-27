import discord
import csv
from discord.ext import commands
import sqlite3
import os
import sys
with open('help.csv', newline='') as f:
    reader = csv.reader(f)
    helpcsv = list(reader)
close = discord.Embed(description='<:zak:704360287750455367> View command list',colour=discord.Colour.from_rgb(47,49,54))
def get_prefix(bot,message):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(message.guild.id))
	try:return commands.when_mentioned_or(c.fetchone()[1])(bot,message)
	except:return commands.when_mentioned_or('!')(bot,message)
def commandlist(message):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(message.guild.id))
	try:prefix=c.fetchone()[1]
	except:prefix='!'
	embed = discord.Embed(description='Keys: (flexible)    [optional]',colour=discord.Colour.from_rgb(47,49,54))
	for row in helpcsv:
		embed.add_field(name=str(prefix)+str(row[0]),value=str(row[1]),inline=False)
	return embed
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command("help")
end=discord.Embed(description='resent `!help`',colour=discord.Colour.from_rgb(47,49,54))
@client.event
async def on_ready():
	global guild,zak
	guild=client.get_guild(486870895978086400)
	zak=client.get_emoji(704360287750455367)
	print('Logged in as '+client.user.name+'\nRunning '+ os.path.basename(__file__))
@client.command(aliases=(['cmd','command','commands','cmds']))
async def help(ctx):
	commands=commandlist(ctx.message)
	helpmessage=await ctx.message.channel.send(embed=close)
	await helpmessage.add_reaction(zak)
	def check(reaction,user):return user != client.user and reaction.emoji==zak and reaction.message.id==helpmessage.id
	try:
		while True:
			reaction,user = await client.wait_for('reaction_add',timeout=60.0,check=check)
			await message.channel.send(embed=commands)
			await message.edit(embed=commands)
			reaction,user = await client.wait_for('reaction_remove',timeout=60.0,check=check)
			await message.edit(embed=close)
	except:
		await message.edit(embed=end)
		await message.clear_reactions()
client.run(open("id.txt", "r").read())