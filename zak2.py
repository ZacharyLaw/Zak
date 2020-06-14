#explore
import discord
import asyncio
import csv
import random
from fuzzywuzzy import process,fuzz
import glob
import time
from datetime import datetime,timedelta,date
import wikia
import pandas as pd
import re
import urllib
import os
import io
import math
import sys
import numpy as np
from PIL import Image
import pathlib
from PIL import Image, ImageDraw, ImageFont
import json
from discord.ext import commands
from os import listdir
from os.path import isfile, join
import sqlite3
fact = [(line.strip()).split() for line in open("fact.txt", "r")]
ship=list(csv.reader(open("ship.csv","r")))
galaxy=list(csv.reader(open("galaxy.csv","r")))
sector=list(csv.reader(open("sector.csv","r")))
generalpd= pd.read_csv('general.csv', index_col=0)
modulepd= pd.read_csv('module.csv', index_col=0)
build=pd.read_csv('build.csv', index_col=0,dtype=str).fillna('')
buildcorrect= pd.read_csv('buildcorrect.csv', index_col=0)
cell=Image.open('cell.png')
def get_prefix(bot,message):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(message.guild.id))
	try:return commands.when_mentioned_or(c.fetchone()[1])(bot,message)
	except:return commands.when_mentioned_or('!')(bot,message)
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days%7}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
def column(matrix, i):
	return [row[i] for row in matrix]
def JPEGSaveWithTargetSize(im, filename, target):
	Qmin, Qmax = 25, 96
	Qacc = -1
	while Qmin <= Qmax:
		m = math.floor((Qmin + Qmax) / 2)
		buffer = io.BytesIO()
		im.save(buffer, format="PNG", quality=m)
		s = buffer.getbuffer().nbytes
		if s <= target:
			Qacc = m
			Qmin = m + 1
		elif s > target:
			Qmax = m - 1
	if Qacc > -1:
		im.save(filename, format="PNG", quality=Qacc) 
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
	x, y = im.size
	size = max(min_size, x, y)
	new_im = Image.new('RGBA', (size, size), fill_color)
	new_im.putalpha(0)
	try:new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)),mask=im)
	except:new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
	return new_im
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()
client = commands.Bot(command_prefix=get_prefix)
#client = commands.Bot(command_prefix=commands.when_mentioned_or(get_prefix))
client.remove_command("help")
@client.event
async def on_ready():
	global guild,corvette,frigate,cruiser,battleship,carrier,suppercarrier,galacticcarrier,unverified,android,ios,pc,ru
	guild=discord.utils.find(lambda g: g.id == 486870895978086400, client.guilds)
	corvette=guild.get_role(515173171742244884)
	frigate=guild.get_role(506117736070381578)
	cruiser=guild.get_role(487742396914991114)
	battleship=guild.get_role(487947882238967820)
	carrier=guild.get_role(496090951056621591)
	suppercarrier=guild.get_role(487052478760747019)
	galacticcarrier=guild.get_role(632508763844116490)
	unverified=guild.get_role(638594355661373460)
	android=guild.get_role(517175120431808523)
	ios=guild.get_role(515299388080390145)
	pc=guild.get_role(558226800296329216)
	ru=guild.get_role(657521436113764352)	
	print('Logged in as '+client.user.name+'\nRunning '+ os.path.basename(__file__))
@client.event
async def on_raw_message_delete(payload):
	if not payload.cached_message.author.bot and not payload.cached_message.content.startswith('!') and payload.cached_message.guild.id==486870895978086400 and not payload.cached_message.channel.id in [567848114170494976,567848114170494976]:
		await  client.get_channel(670483927537811457).send(payload.cached_message.channel.mention+': '+payload.cached_message.author.mention+':\n> '+payload.cached_message.content)
		if len(payload.cached_message.attachments)>0:
			open('temp.png', 'wb').write(requests.get(payload.cached_message.attachments[0].proxy_url).content)
			await client.get_channel(670483927537811457).send(file=discord.File('temp.png'))	
			os.remove('temp.png')
@client.event
async def on_guild_remove(guild):
	with open('prefixes.json','r') as f:
		prefix=json.load(f)
	prefix.pop(str(guild.id))
	with open('prefixes.json','w') as f:
		json.dump(prefixes,f,indent=4)
@client.command()
async def prefix(ctx,prefix):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(ctx.guild.id))
	if 	c.fetchone():
		c.execute("""DELETE FROM prefixes WHERE id="""+str(ctx.guild.id))
		c.execute("""INSERT INTO prefixes VALUES (?,?)""",(ctx.guild.id,prefix))
	else:c.execute("""INSERT INTO prefixes VALUES (?,?)""",(ctx.guild.id,prefix))
	conn.commit()
	await ctx.message.add_reaction('👌')

@client.command(aliases=(['w','wiki']))
async def wikia(ctx,arg):await ctx.send(embed=discord.Embed(description='Wikia Search result:\n['+' '.join(map(str, wikia.search('spacearena',arg,1)))+'](http://spacearena.fandom.com/wiki/'+' '.join(map(str, wikia.search('spacearena',arg,1))).replace(' ','_')+')',colour=discord.Colour.from_rgb(47,49,54)))
@client.command()
async def zak(ctx):await ctx.message.add_reaction('👋')
@client.command()
async def fact(ctx):await ctx.send(' '.join(random.choice(fact)))
@client.command()
async def invite(ctx):await ctx.send(embed =discord.Embed(description='Zak Invite Link\n[link](https://discordapp.com/oauth2/authorize?client_id=563319785811869698&scope=bot)'))
@client.command()
async def about(ctx):await ctx.send(embed =discord.Embed(description='<@563319785811869698> is made by <@270864978569854976>\nFor the Space Arena Offical Server\nBorn at 10/12/2019\nNice to meet you Senpi!\n[Github](http://github.com/ZacharyLaw/Zak)',colour=discord.Colour.from_rgb(47,49,54)))
@client.command()
async def sector(ctx,*,arg):
	args=arg.split(' ')
	if '.' in args[0]:args=arg.split(' ')[0].split('.')
	await ctx.send('Sector '+str(args[1])+'.'+str(args[2])+' '+data[(int(args[1])-1)*10+int(args[2])-1][5]+'\n<:ballistic:570222613180186653>'+data[(int(args[1])-1)*10+int(args[2])-1][0]+'/19\n<:missile:570222563779936256>'+data[(int(args[1])-1)*10+int(args[2])-1][1]+'/19\n<:laser:570222555802107905>'+data[(int(args[1])-1)*10+int(args[2])-1][2]+'/19\n<a:armor:654546483613270017>'+data[(int(args[1])-1)*10+int(args[2])-1][3]+'/19\n<a:shield:654546575858860043>'+data[(int(args[1])-1)*10+int(args[2])-1][4]+'/19')
@client.command()
async def guide(ctx):await ctx.send('https://cdn.discordapp.com/attachments/566268214514941952/684388364337676516/guide.gif')
@client.command()
async def stonk(ctx):await ctx.send(file=discord.File('stonk.png'))
@client.command(aliases=(['weapon']))
async def weap(ctx):await ctx.send(file=discord.File('weap.png'))
@client.command(aliases=(['upgrade']))
async def upg(ctx):await ctx.send(file=discord.File('upg6.png'))
@client.command()
async def cou(ctx):await ctx.send(file=discord.File('counter4.png'))
@client.command()
async def combo(ctx):await ctx.send(file=discord.File('combo.png'))
@client.command()
async def shipupg(ctx):await ctx.send(file=discord.File('shipupg3.png'))
@client.command(aliases=(['ships']))
async def ship(ctx):await ctx.send(file=discord.File('ship.png'))
@client.command()
async def mod(ctx):await ctx.send(file=discord.File('mod.png'))
@client.command()
async def time(ctx):await ctx.send('Daily quest & Daily Deals countdown: '+strfdelta(datetime(2011, 5, 5,13) - datetime.now(),'{hours}h {minutes}m')+'\nClass Battle countdown: '+strfdelta(datetime(2020, 6, 15,12) - datetime.now(),'{days}d {hours}h {minutes}m')+'\nHeroCraft HQ Time: '+(datetime.today()).strftime("%H:%M"))
@client.command()
async def cell(ctx,*,arg):
	filename=str(buildcorrect.loc[str(process.extractOne(arg,buildcorrect.index.values ,score_cutoff=80)[0]),'Filename'])
	if filename=='nan':filename=str(buildcorrect.loc[str(buildcorrect.loc[str(process.extractOne(arg,buildcorrect.index.values ,score_cutoff=80)[0]),'Alternative']),'Filename'])
	await ctx.send(file=discord.File('/home/zak/Zak/cell/'+filename+'.png'))
@client.command(aliases=(['price']))
async def cost(ctx,*,arg):
	index=''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2'),generalpd.index.values,score_cutoff=80)[0])) 
	if str(generalpd.loc[index,'Alternative'])!='nan': index=str(generalpd.loc[index,'Alternative'])
	msg=str(index)+'\n'
	if str(generalpd.loc[index,'Acquisition'])!='nan':msg+='Acquisition: '+str(generalpd.loc[index,'Acquisition'])
	elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])=='nan' and str(generalpd.loc[index,'Blueprint'])=='nan':msg+='Cost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
	elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])!='nan':msg+='Cost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481> / '+str(generalpd.loc[index,'Celestium'])+'<:celes:570222210476670976>'
	elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Blueprint'])!='nan':msg+='Cost: '+str(int(generalpd.loc[index,'Blueprint']))+'<:blueprint:568688146683002880> & '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
	await ctx.send(msg)		
@client.command()
async def meme(ctx):await ctx.send(file=discord.File('/home/zak/Zak/meme/'+str(random.choice([f for f in listdir('C:\$Zac\spacearena\Zak\meme') if isfile(join('C:\$Zac\spacearena\Zak\meme', f))]))))
@client.command()
async def info(ctx,*,arg):
	if ' vs ' in arg:
		indexs=[''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2').split(' vs ')[0],generalpd.index.values,score_cutoff=80)[0])) , ''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2').split(' vs ')[1],generalpd.index.values,score_cutoff=80)[0]))]
		indexs=[ str(generalpd.loc[index,'Alternative']) if str(generalpd.loc[index,'Alternative'])!='nan' else index for index in indexs]
		await ctx.send('```'+generalpd.loc[indexs].transpose().drop('Upgradeable Bonus').dropna(how='all').fillna('').replace(to_replace=r'<:celes:570222210476670976\S',value='celes',regex=True).to_string()+'```')
	else:
		index=''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2'),generalpd.index.values,score_cutoff=80)[0])) 
		if str(generalpd.loc[index,'Alternative'])!='nan': index=str(generalpd.loc[index,'Alternative'])
		page1=str(index)+' <:1one:714760225466482689>\nLevel: '+str(int(generalpd.loc[index,'Level']))
		if str(generalpd.loc[index,'Acquisition'])!='nan':page1+='\nAcquisition: '+str(generalpd.loc[index,'Acquisition'])
		elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])=='nan' and str(generalpd.loc[index,'Blueprint'])=='nan':page1+='\nCost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
		elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])!='nan':page1+='\nCost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481> / '+str(generalpd.loc[index,'Celestium'])+'<:celes:570222210476670976>'
		elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Blueprint'])!='nan':page1+='\nCost: '+str(int(generalpd.loc[index,'Blueprint']))+'<:blueprint:568688146683002880> & '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
		page2=str(index)+' <:2two:714760495458156675>'
		for title in ['Speed','Turning','Cell','Max','Support','Supp. Cell','Supp. Max','Size','Power Use','Health','Armor','Mass','Reflect']:
			if str(generalpd.loc[index,title])!='nan':
				try:page2+='\n'+title+': '+str(int(generalpd.loc[index,title]))
				except:page2+='\n'+title+': '+str(generalpd.loc[index,title])
		page3=str(index)+' <:3three:714760505797115905>'
		for title in ['Mod 1','Mod 2','Mod 3','Mod 4','Mod 5','Supp. Mod 1','Supp. Mod 2','Supp. Mod 3','Supp. Mod 4','Supp. Mod 5','Anti Penetration Damage','Power Generation','Explosion Damage','Explosion Radius','Damage','Range','Fire Cone','Fire Rate','Penetrating Damage','No. of Missiles','Rocket Explosion Radius','Flight Time','No. of Mines','Mines Explosion Radius','Mine Lifespan','Laser Duration','Max Regeneration','Regen Speed','Shield Radius','Shield Strength','Junk Amount','Junk Flight Time','Mine Disruption %','Rocket Disruption %','Torpedo Disruption %','Thrust Power','Warp Force','Duration','Thrust Boost','Turning Boost','Max Module']:
			if str(generalpd.loc[index,title])!='nan':page3+='\n'+title+': '+str(generalpd.loc[index,title])
		page4=str(index)+' <:4four:714760514189787139>'
		if str(generalpd.loc[index,'Upgradeable Bonus'])!='nan':page4+='\nUpgradeable Bonus:\n'+str(generalpd.loc[index,'Upgradeable Bonus'])
		if str(generalpd.loc[index,'Unique Bonus'])!='nan':page4+='\nUnique Bonus: '+str(generalpd.loc[index,'Unique Bonus'])
		message=await ctx.channel.send(page1)
		if '\n' in page1: await message.add_reaction('<1one:714760225466482689>')
		if '\n' in page2: await message.add_reaction('<2two:714760495458156675>')
		if '\n' in page3: await message.add_reaction('<3three:714760505797115905>')
		if '\n' in page4: await message.add_reaction('<4four:714760514189787139>')
		def check(reaction,user):return user.id!=563319785811869698
		try:
			while True:
				reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
				if reaction.message.id==message.id:
					if reaction.emoji.id==714760225466482689 and '\n' in page1:await message.edit(content=page1)
					elif reaction.emoji.id==714760495458156675 and '\n' in page2:await message.edit(content=page2)
					elif reaction.emoji.id==714760505797115905 and '\n' in page3:await message.edit(content=page3)
					elif reaction.emoji.id==714760514189787139 and '\n' in page4:await message.edit(content=page4)
				await message.remove_reaction(reaction,user)
			await message.clear_reactions()
		except:await message.clear_reactions()					
"""@client.event
async def on_message(message):
	if message.author.id in [275813801792634880,234395307759108106,365975655608745985]:
		if (message.author.id==275813801792634880 and message.channel.id!=567848114170494976 and message.channel.id!=551580844289032202) or (message.author.id==234395307759108106 and message.embeds[0].description.startswith('Groovy is the easiest way')) or (message.author.id in 234395307759108106 and message.embeds[0].description.startswith('You must be playing a track to use this command!')) or (message.author.id==365975655608745985 and message.embeds[0].title.startswith('Congratulations')):await message.delete()
	if message.content.islower() and message.channel.id==650285845487550464:await message.delete()"""

client.run(open("id.txt", "r").read())