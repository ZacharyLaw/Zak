import discord
import pandas as pd
import os
import sys
import re
import csv
import sqlite3
from discord.ext import commands
def get_prefix(bot,message):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(message.guild.id))
	try:return commands.when_mentioned_or(c.fetchone()[1])(bot,message)
	except:return commands.when_mentioned_or('!')(bot,message)
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command("help")
profilepd=pd.read_csv('profile.csv', index_col=0,dtype=str)
profilepd['Facebook']='[Link]('+profilepd['Fb']+')'
@client.event
async def on_ready():print('Logged in as '+client.user.name+'\nRunning '+ os.path.basename(__file__))
@client.command()
async def profile(ctx,*args):
	message=ctx.message
	if len(message.content.split(' '))==1:
		try:
			authorprofile=profilepd.loc[[message.author.id]]
			msg=authorprofile[['IGN','SupportID','Facebook']].transpose().dropna().to_string(header=False).replace('  ','').replace('IGN','IGN: ').replace('SupportID','SupportID: ').replace('Facebook','Facebook: ')
			if not  'Facebook: ' in msg:await message.channel.send(msg)
			else:
				embed = discord.Embed(description=msg,colour=discord.Colour.from_rgb(47,49,54))
				await message.channel.send(embed=embed)
		except:await message.channel.send('Profile not found')
	elif message.mentions:
		try:
			authorprofile=profilepd.loc[[message.mentions[0].id]]
			msg=authorprofile[['IGN','SupportID','Facebook']].transpose().dropna().to_string(header=False).replace('  ','').replace('IGN','IGN: ').replace('SupportID','SupportID: ').replace('Facebook','Facebook: ')
			if not  'Facebook: ' in msg:await message.channel.send(msg)
			else:
				embed = discord.Embed(description=msg,colour=discord.Colour.from_rgb(47,49,54))
				await message.channel.send(embed=embed)
		except:await message.channel.send('Profile not found')
	elif message.author.id==270864978569854976:
		if re.findall('\S{4,16}',' '.join(args))[0] in profilepd.index:profilepd.loc[re.findall('\S{4,16}',' '.join(args))[0],'IGN']=re.findall('\S{4,16}',' '.join(args))[0]
		else:profilepd.loc[re.findall('\S{4,16}',arg)[0]]=[re.findall('\S{4,16}',arg)[0],None,None,None]
	else:
		for arg in args:#ign,support,fb
			if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',arg):
				if message.author.id in profilepd.index:profilepd.loc[message.author.id,'Fb']=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content)[0]
				else:profilepd.loc[message.author.id]=[None,None,re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content)[0],None]
				os.remove('profile.csv')
				profilepd[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
			elif re.findall('\S{4,16}',arg):				
				if message.author.id in profilepd.index:profilepd.loc[message.author.id,'IGN']=re.findall('\S{4,16}',arg)[0]
				else:profilepd.loc[message.author.id]=[re.findall('\S{4,16}',arg)[0],None,None,None]
				os.remove('profile.csv')
				profilepd[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
			elif re.findall('\d{16}',arg):
				if message.author.id in profilepd.index:profilepd.loc[message.author.id,'SupportID']=re.findall('\d{16}',arg)[0]
				else:profilepd.loc[message.author.id]=[None,re.findall('\d{16}',arg)[0],None,None]
				os.remove('profile.csv')
				profilepd[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
client.run(open("id.txt", "r").read())