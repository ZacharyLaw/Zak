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
from tabulate import tabulate
import requests
fact = [(line.strip()).split() for line in open("fact.txt", "r")]
ship=list(csv.reader(open("ship.csv","r")))
galaxy=list(csv.reader(open("galaxy.csv","r")))
sector=list(csv.reader(open("sector.csv","r")))
general= pd.read_csv('general.csv', index_col=0)
modulepd= pd.read_csv('module.csv', index_col=0)
buildpd=pd.read_csv('build.csv', index_col=0,dtype=str).fillna('')
buildcorrect= pd.read_csv('buildcorrect.csv', index_col=0)
dict={714760225466482689:1,714760495458156675:2,714760505797115905:3,714760514189787139:4,714760523027185794:5}
react={1:'1one:714760225466482689',2:'2two:714760495458156675',3:'3three:714760505797115905',4:'4four:714760514189787139',5:'5five:714760523027185794',6:'6six:714769193517449257'}
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
async def reactionadd():
	def check(reaction,user):return user.id!=563319785811869698
	reaction, user= await client.wait_for('reaction_add' , timeout=180.0, check=check)
	return reaction,user
async def reactionremove():
	def check(reaction,user):return user.id!=563319785811869698
	reaction, user= await client.wait_for('reaction_remove' , timeout=180.0, check=check)
	return reaction,user
async def modulemessage():
	def check(m):return m.author.id!=563319785811869698 and m.content.startswith('+')
	msg = await client.wait_for('message', timeout=180.0, check=check)
	return msg
def horizontal_resize_merge(im1fn, im2fn,filename, resample=Image.BICUBIC, resize_big_image=True):
	im1 = Image.open(im1fn)
	im2 = Image.open(im2fn)
	if im1.height == im2.height:
		_im1 = im1
		_im2 = im2
	elif (((im1.height > im2.height) and resize_big_image) or
		  ((im1.height < im2.height) and not resize_big_image)):
		_im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
		_im2 = im2
	else:
		_im1 = im1
		_im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
	dst = Image.new('RGB', (_im1.width + int(_im2.width*0.8), _im1.height))
	dst.putalpha(0)
	dst.paste(_im1, (0, 0))
	dst.paste(_im2.resize((int(_im2.width*0.8),int(_im2.height*0.8)), resample=resample), (_im1.width, 0))
	dst.save(filename)
async def administrator(ctx):
	return ctx.message.author.guild_permissions.administrator
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command("help")
@client.event
async def on_ready():
	global botchannel
	botchannel=client.get_channel(674632751390916609)
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
@commands.check(administrator)
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
	index=''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2'),general.index.values,score_cutoff=80)[0])) 
	if str(general.loc[index,'Alternative'])!='nan': index=str(general.loc[index,'Alternative'])
	msg=str(index)+'\n'
	if str(general.loc[index,'Acquisition'])!='nan':msg+='Acquisition: '+str(general.loc[index,'Acquisition'])
	if str(general.loc[index,'Cost'])!='nan':msg+='Cost: ' +str(general.loc[index,'Cost'])
	await ctx.send(msg)		
@client.command()
async def meme(ctx):await ctx.send(file=discord.File('/home/zak/Zak/meme/'+str(random.choice([f for f in listdir('C:\$Zac\spacearena\Zak\meme') if isfile(join('C:\$Zac\spacearena\Zak\meme', f))]))))
@client.command()
async def info(ctx,*,arg):
	if ' vs ' in arg:
		indexs=[''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2').split(' vs ')[0],general.index.values,score_cutoff=80)[0])) , ''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2').split(' vs ')[1],general.index.values,score_cutoff=80)[0]))]
		indexs=[ str(general.loc[index,'Alternative']) if str(general.loc[index,'Alternative'])!='nan' else index for index in indexs]
		try:await ctx.send('```'+general.loc[indexs].transpose().dropna(how='all').fillna('').replace(to_replace=r'<:celes:570222210476670976\S',value='celes',regex=True).replace(to_replace=r'<:bp:568688146683002880\S',value='bp',regex=True).replace(to_replace=r'Total Module',value='',regex=True).to_string().replace('Index','	 ')+'```')
		except:
			page1='```'+general.loc[indexs].transpose().drop('Upgradeable Bonus').dropna(how='all').fillna('').replace(to_replace=r'<:celes:570222210476670976\S',value='celes',regex=True).replace(to_replace=r'<:bp:568688146683002880\S',value='bp',regex=True).replace(to_replace=r'Total Module',value='',regex=True).to_string().replace('Index','	 ')+'```'
			page2='```Upgradeable Bonus\n'+tabulate([indexs,[general.loc[indexs[0],'Upgradeable Bonus'],general.loc[indexs[1],'Upgradeable Bonus']]],tablefmt="plain")+'```'
			message=await ctx.channel.send(page1)
			await message.add_reaction('<1one:714760225466482689>')
			await message.add_reaction('<2two:714760495458156675>')
			def check(reaction,user):return user.id!=563319785811869698
			try:
				while True:
					reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
					if reaction.message.id==message.id:
						if reaction.emoji.id==714760225466482689:await message.edit(content=page1)
						elif reaction.emoji.id==714760495458156675:await message.edit(content=page2)
					await message.remove_reaction(reaction,user)
				await message.clear_reactions()
			except:await message.clear_reactions()					
	else:
		index=''.join(map(str,process.extractOne(arg.replace('mkiii','mk3').replace('mkii','mk2'),general.index.values,score_cutoff=80)[0])) 
		if str(general.loc[index,'Alternative'])!='nan': index=str(general.loc[index,'Alternative'])
		page1=str(index)+' <:1one:714760225466482689>\nLevel: '+str(int(general.loc[index,'Level']))
		if str(general.loc[index,'Acquisition'])!='nan':page1+='\nAcquisition: '+str(general.loc[index,'Acquisition'])
		if str(general.loc[index,'Cost'])!='nan':page1+='\nCost: ' +str(general.loc[index,'Cost']).replace('cred','<:credit:570222178348564481>').replace('celes','<:celes:570222210476670976>').replace('bp','<:bp:568688146683002880>')
		page2=str(index)+' <:2two:714760495458156675>'
		for title in ['Speed','Turning','Cell','Max','Support','Supp. Cell','Supp. Max','Size','Power Use','Health','Armor','Mass','Reflect']:
			if str(general.loc[index,title])!='nan':
				try:page2+='\n'+title+': '+str(int(general.loc[index,title]))
				except:page2+='\n'+title+': '+str(general.loc[index,title])
		page3=str(index)+' <:3three:714760505797115905>'
		for title in ['Mod 1','Mod 2','Mod 3','Mod 4','Mod 5','Supp. Mod 1','Supp. Mod 2','Supp. Mod 3','Supp. Mod 4','Supp. Mod 5','Anti Penetration Damage','Power Generation','Explosion Damage','Explosion Radius','Damage','Range','Fire Cone','Fire Rate','Penetrating Damage','No. of Missiles','Rocket Explosion Radius','Flight Time','No. of Mines','Mines Explosion Radius','Mine Lifespan','Laser Duration','Max Regeneration','Regen Speed','Shield Radius','Shield Strength','Junk Amount','Junk Flight Time','Mine Disruption %','Rocket Disruption %','Torpedo Disruption %','Thrust Power','Warp Force','Duration','Thrust Boost','Turning Boost','Max Module']:
			if str(general.loc[index,title])!='nan':page3+='\n'+title+': '+str(general.loc[index,title])
		page4=str(index)+' <:4four:714760514189787139>'
		if str(general.loc[index,'Upgradeable Bonus'])!='nan':page4+='\nUpgradeable Bonus:\n'+str(general.loc[index,'Upgradeable Bonus'])
		if str(general.loc[index,'Unique Bonus'])!='nan':page4+='\nUnique Bonus: '+str(general.loc[index,'Unique Bonus'])
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
@client.command(aliases=(['energy']))
async def power(ctx,*,arg):
	content=arg.replace('mkiii','mk3').replace('mkii','mk2')
	usage=0
	energy=0
	for spliter in content.split(','):
		if spliter[0]==' ':spliter=spliter[1:]
		amount=spliter.split(' ', 1)[0]
		item=''.join(map(str,process.extractOne(spliter.split(' ', 1)[1],general.index.values,score_cutoff=80)[0])) 
		if str(general.loc[item,'Alternative'])!='nan': item=str(general.loc[item,'Alternative'])
		if str(general.loc[item,'Power Use'])!='nan':usage+=int(general.loc[item,'Power Use'])*int(amount)
		elif str(general.loc[item,'Power Generation'])!='nan':energy+=int(general.loc[item,'Power Generation'])*int(amount)
		try:
			if int(energy/usage)*100>100:percent='100%: '
			else:percent=str(int(energy/usage*100))+'%: '
		except:percent='100%: '
	await ctx.send(percent+str(usage)+'/'+str(energy))   
@client.command()
async def shop(ctx,*args):
	arg=' '.join(args)
	if arg=='':await ctx.send('`!shpp [item] x[quanity] [price]celes [image link]`\nEg : `!shop Infinity Gauntlet x1 999celes http:// ... .png')
	else:
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', args.content)
		price=quanity=msg=' '
		for word in arg.content.split(' '):
			if 'celes' in word:price=word.split('celes')[0]
			elif 'x' in word[0]:quanity=word
		msg=arg.split(quanity)[0]
		if price==' ' or quanity==' ' or msg==' ':await ctx.send('Missing arguement(s)\n`!shpp [item] x[quanity] [price]celes [image link]`\nEg : `!shop Infinity Gauntlet x1 999celes http:// ... .png`')
		elif len(urls)==0:await ctx.channel.send('No image recieved')
		else:
			preshop = Image.open("preshop.png")
			open('item.png', 'wb').write(requests.get(urls[0]).content)
			draw = ImageDraw.Draw(preshop)
			font = ImageFont.truetype('arial.ttf',40)
			w, h = draw.textsize(msg,font=font)
			draw.text(((1080+680-w)/2,(1440+305-h)/2),msg.capitalize(),(255,255,255),font=font,align="center")
			font = ImageFont.truetype('arial.ttf',50)
			w, h = draw.textsize(quanity,font=font)
			draw.text(((1080+680-w)/2,(1440+430-h)/2),quanity,(30,243,243),font=font,align="center")
			font = ImageFont.truetype('arial.ttf',50)
			w, h = draw.textsize(price,font=font)
			draw.text((855,1215),price,(255,255,255),font=font,align="centre")
			item=make_square(Image.open('item.png'),min_size=175)
			resized=item.resize((175,175))
			preshop.paste(resized,(790,1000),mask=resized)
			preshop.save('shop.png')
			await ctx.send(file=discord.File('shop.png'))
@client.command()
async def creator(ctx):
	global usage,energy,width,height
	cell=Image.open('cell.png')
	cursor=Image.open('cursor.png').convert("RGBA")
	null=Image.new('RGB', (100,100))
	null.putalpha(0)
	xcoord=ycoord=1
	image = Image.new('RGB', (100,100))
	image.putalpha(0)
	image.save('create.png')
	image.paste(cursor,(0,0),mask=cursor)
	image.save('cursored.png')
	channel=ctx.channel
	embed = discord.Embed(description='Build Creator',colour=discord.Colour.from_rgb(47,49,54))
	embed.set_image(url='https://cdn.discordapp.com/attachments/674632751390916609/701451643404943421/cursored.png')
	embed.set_footer(text='+(module name)   Adds module at cursor position',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
	creator=await channel.send(embed=embed)
	await creator.add_reaction('<:hide:701459826328207613>')#hide cursor
	await creator.add_reaction('⬆️')
	await creator.add_reaction('⬇️')
	await creator.add_reaction('⬅️')
	await creator.add_reaction('➡️')
	await creator.add_reaction('<:null:690865781071675412>')#null
	await creator.add_reaction('<:base:690840728489820191>')#base
	hide=usage=energy=lock=0
	#try:
	if True:
		while True:
			add = asyncio.create_task(reactionadd())
			rem = asyncio.create_task(reactionremove())
			msg = asyncio.create_task(modulemessage())
			done, pending = await asyncio.wait([add,rem,msg], return_when=asyncio.FIRST_COMPLETED)
			if add in done: action=0
			if rem in done: action=-1
			if msg in done: action=1
			if action in [0,-1]:reaction, user= done.pop().result()
			else:message=done.pop().result()
			if action==0:
				create=Image.open('create.png').convert("RGBA")
				width,height=create.size
				if reaction.emoji=='⬆️':
					if ycoord==1:
						extend=Image.new('RGB', (width,height+100))
						extend.putalpha(0)
						extend.paste(create,(0,100),mask=create)
						if lock==1:extend.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
						extend.save('create.png')
						cursored = extend.copy() 
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					else:
						ycoord-=1
						if lock==1:
							create.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
							create.save('create.png')
						cursored = create.copy() 
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					await creator.remove_reaction(reaction,user) 
				elif reaction.emoji=='⬇️':
					if height/100==ycoord:
						ycoord+=1
						extend=Image.new('RGB', (width,height+100))
						extend.putalpha(0)
						extend.paste(create,(0,0),mask=create)
						if lock==1:extend.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
						extend.save('create.png')
						cursored = extend.copy() 
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					else:
						ycoord+=1
						if lock==1:
							create.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
							create.save('create.png')
						cursored = create.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					await creator.remove_reaction(reaction,user) 
				elif reaction.emoji=='⬅️':
					if xcoord==1:
						extend=Image.new('RGB', (width+100,height))
						extend.putalpha(0)
						extend.paste(create,(100,0),mask=create)
						if lock==1:extend.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
						extend.save('create.png')
						cursored = extend.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					else:
						xcoord-=1
						if lock==1:
							create.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
							create.save('create.png')
						cursored = create.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					await creator.remove_reaction(reaction,user) 
				elif reaction.emoji=='➡️':
					if width/100==xcoord:
						xcoord+=1
						extend=Image.new('RGB', (width+100,height))
						extend.putalpha(0)
						extend.paste(create,(0,0),mask=create)
						if lock==1:extend.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
						extend.save('create.png')
						cursored = extend.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					else:
						xcoord+=1
						if lock==1:
							create.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
							create.save('create.png')
						cursored = create.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
					await creator.remove_reaction(reaction,user) 
				elif reaction.emoji.id==690840728489820191:#base
					create.paste(cell,((xcoord-1)*100,(ycoord-1)*100))
					create.save('create.png')
					cursored = create.copy()
					cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
					cursored.save('cursored.png')
					lock=1
				elif reaction.emoji.id==690865781071675412:#null
					create.paste(null,((xcoord-1)*100,(ycoord-1)*100))
					create.save('create.png')
					cursored = create.copy()
					cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
					cursored.save('cursored.png')
					await creator.remove_reaction(reaction,user)
				elif reaction.emoji.id==701459826328207613:#hide
					if not hide:
						create.save('cursored.png')
						hide=1
						embed.set_footer(text='',icon_url='')
						await creator.clear_reactions()
						await creator.add_reaction('<:hide:701459826328207613>')#hide cursor
					elif hide:
						hide=0
						await creator.add_reaction('⬆️')
						await creator.add_reaction('⬇️')
						await creator.add_reaction('⬅️')
						await creator.add_reaction('➡️')
						await creator.add_reaction('<:null:690865781071675412>')#null
						await creator.add_reaction('<:base:690840728489820191>')#base
						create.save('create.png')
						cursored = create.copy()
						cursored.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
						cursored.save('cursored.png')
						embed.set_footer(text='+(module name)   Adds module at cursor position',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
						await creator.remove_reaction(reaction,user)
				message=await botchannel.send(file=discord.File('cursored.png'))
				embed.set_image(url=message.attachments[0].url)
				await creator.edit(embed=embed)
			elif action==-1 and reaction.emoji.id==690840728489820191:lock=0#base
			elif action==1:
				module=Image.open(str(pathlib.Path().absolute())+'/module/'+str(modulepd.loc[str(process.extractOne(message.content.split('+',1)[1],modulepd.index.values ,score_cutoff=80)[0]),'Filename'])+'.png')
				create=Image.open('create.png').convert("RGBA")
				create.paste(module,((xcoord-1)*100,(ycoord-1)*100)) 
				create.save('create.png')
				create.paste(cursor,((xcoord-1)*100,(ycoord-1)*100),mask=cursor)
				create.save('cursored.png')       
				item=''.join(map(str,process.extractOne(message.content.split('+',1)[1],generalpd.index.values,score_cutoff=80)[0])) 
				if str(generalpd.loc[item,'Alternative'])!='nan': item=str(generalpd.loc[item,'Alternative'])
				if str(generalpd.loc[item,'Power Use'])!='nan':usage+=int(generalpd.loc[item,'Power Use'])
				elif str(generalpd.loc[item,'Power Generation'])!='nan':energy+=int(generalpd.loc[item,'Power Generation'])
				try:
					if int(energy/usage)*100>100:percent='100%: '
					else:percent=str(int(energy/usage*100))+'%: '
				except:percent='100%: '
				message=await botchannel.send(file=discord.File('cursored.png'))
				embed = discord.Embed(description=percent+str(usage)+'/'+str(energy),colour=discord.Colour.from_rgb(47,49,54))
				embed.set_image(url=message.attachments[0].url)
				embed.set_footer(text='+(module name)   Adds module at cursor position',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
				await creator.edit(embed=embed)
		await creator.clear_reactions()
		embed.set_footer(text='',icon_url='')
		await creator.edit(embed=embed)
	
	#except:await creator.clear_reactions()			
@client.command(aliases=(['submitbuild']))
async def submit(ctx,*,arg):
	sender=ctx
	try:
		if re.findall('https://p?t?b?.?discordapp.com/channels/\d+/\d+/\d+',arg):
			msglink=re.findall('https://p?t?b?.?discordapp.com/channels/\d+/\d+/\d+',arg)[0]
			message=await client.get_channel(int(msglink.split('/')[5])).fetch_message(int(msglink.split('/')[6]))
			shipname=re.sub(r"http\S+", "", arg)
			desc='\n'+message.content
		else:
			message=ctx.message
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', arg)
			if ',' in arg:shipname=re.sub(r"http\S+", "",  arg.split(',',1)[0])
			elif ',' not in arg:shipname=re.sub(r"http\S+", "",  arg)				
			if ',' not in arg:desc=''
			else:desc=re.sub(r"http\S+", "",  arg.split(',',1)[1])			
		if len(ctx.message.attachments)==0 and len(urls)==0:await sender.send('No image recieved')
		elif shipname=='':await sender.send('No shipname received')
		elif not (process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80) or process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)):await sender.channel.send('Shipname not found')
		else:
			if len(urls)==0 and len(ctx.message.attachments)==2:urls=[ctx.message.attachments[0].url,ctx.message.attachments[1].url]
			elif len(urls)==0 and len(ctx.message.attachments)==1:urls=[ctx.message.attachments[0].url]
			if process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80):
				filename=str(buildcorrect.loc[process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)[0],'Filename'])
				index=str(process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)[0])
			elif process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80):
				filename=str(buildcorrect.loc[process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)[0],'Filename'])
				index=str(process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)[0])
			if str(buildcorrect.loc[index,'Alternative'])!='nan':
				index=str(buildcorrect.loc[index,'Alternative'])
				filename=str(buildcorrect.loc[index,'Filename'])
			for x in range(50):
				if not filename+str(x+1) in buildpd.index:
					filename=filename+str(x+1)+'.png'
					break
			open(filename, 'wb').write(requests.get(urls[0]).content)
			if len(urls)==2:
				open('temp.png', 'wb').write(requests.get(urls[1]).content)
				horizontal_resize_merge(filename, 'temp.png',filename)
				os.remove('temp.png')
			screenshot=await botchannel.send(file=discord.File(filename))
			os.remove(filename)
			desc2='\n' if desc=='' else ''+desc
			embed = discord.Embed(description=index+'\nAuthor: '+str(message.author)+'\n'+str(message.created_at.strftime("%d/%m/%Y"))+desc2,colour=discord.Colour.from_rgb(47,49,54))
			embed.set_image(url=screenshot.attachments[0].url)
			embed.set_footer(text='✅ To Confirm',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
			try:
				confirm=await sender.send(embed=embed)
				def check(reaction,user):return user == sender.author and reaction.emoji=='✅'
				await confirm.add_reaction('✅')
				reaction,user = await client.wait_for('reaction_add',check=check,timeout=60.0)
				buildpd.loc[filename.replace('.png','')]=[str(screenshot.attachments[0].id),str(message.author.id),str(message.created_at.strftime("%d/%m/%Y")),desc,'','']
				os.remove('build.csv')
				buildpd.to_csv('build.csv')
				embed.set_footer(text='Submitted')
				await confirm.edit(embed=embed)
				await confirm.clear_reactions()
			except:
				embed.set_footer(text='Failed Submit')
				await confirm.edit(embed=embed)
				await confirm.clear_reactions()
	except discord.errors.Forbidden:await sender.channel.send('Missing permission')
@client.command(aliases=(['b']))
async def build(ctx,*,arg):
	message=ctx.message
	if process.extractOne(message.content,buildcorrect.index.values ,score_cutoff=75) or process.extractOne(arg[1],buildcorrect.index.values ,score_cutoff=80):
		if process.extractOne(message.content,buildcorrect.index.values ,score_cutoff=75):
			filename=str(buildcorrect.loc[process.extractOne(message.content,buildcorrect.index.values ,score_cutoff=80)[0],'Filename'])
			index=str(process.extractOne(message.content,buildcorrect.index.values ,score_cutoff=75)[0])
		elif process.extractOne(arg[1],buildcorrect.index.values ,score_cutoff=75):
			filename=str(buildcorrect.loc[process.extractOne(arg[1],buildcorrect.index.values ,score_cutoff=80)[0],'Filename'])
			index=str(process.extractOne(arg[1],buildcorrect.index.values ,score_cutoff=75)[0])
		if str(buildcorrect.loc[index,'Alternative'])!='nan':
			index=str(buildcorrect.loc[index,'Alternative'])
			filename=str(buildcorrect.loc[index,'Filename'])
	ship=buildpd.loc[buildpd.index.str.startswith(filename)]
	ship['Ratio']=[ 0.5 if str(row.Upvote).count('.')==0 and str(row.Downvote).count('.')==0 else str(row.Upvote).count('.')/(str(row.Upvote).count('.')+str(row.Downvote).count('.'))  for index, row in ship.iterrows() ]
	ship.sort_values('Ratio',ascending=False)
	page=1
	try:author=str(client.get_user(int(ship.iloc[0,1])))
	except:author='Unknown'
	if str(ship.iloc[0,3])=='nan':desc=''
	else:desc='\n'+str(ship.iloc[0,3])
	if message.channel.id in [487232049938300939,487232049938300939,683680285434445914]:selfdestruct=180.0
	else:selfdestruct='test'
	embed = discord.Embed(description=index+' 1/'+str(len(ship))+'\n👍'+str(int(ship.iloc[0,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[0,2])+desc,colour=discord.Colour.from_rgb(47,49,54))
	embed.set_image(url='https://cdn.discordapp.com/attachments/674632751390916609/'+str(ship.iloc[0,0])+'/'+str(ship.head().index[0])+'.png')
	embed.set_footer(text='Up/Downvote    Select Build',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
	msg=await message.channel.send(embed=embed,delete_after=selfdestruct)
	embed.set_footer(text='')
	await msg.add_reaction('<:upvote:592757143892000769>')
	await msg.add_reaction('<:downvote:592757119069978644>')
	if len(ship)==1:pass
	elif len(ship)<7:
		for x in range(len(ship)):await msg.add_reaction('<:'+react[x+1]+'>')
	else:
		for x in range(4):await msg.add_reaction('<:'+react[x+1]+'>')
		await msg.add_reaction('◀️')
		await msg.add_reaction('▶️')
	def check(reaction,user):return user != client.user and reaction.message.id==msg.id
	#try:
	if True:
		while True:
			reaction,user = await client.wait_for('reaction_add',timeout=180.0,check=check)
			if reaction.emoji=='◀️':
				if page!=1:page-=1
				try:author=str(client.get_user(int(ship.iloc[page-1,1])))
				except:author='Unknown'
				if str(ship.iloc[page-1,4])=='nan':desc=''
				else:desc='\n'+str(ship.iloc[page-1,4])
				embed.description=index+' '+str(page)+'/'+str(len(ship))+'\n👍'+str(int(ship.iloc[page-1,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[page-1,2])+desc
				embed.set_image(url='https://cdn.discordapp.com/attachments/674632751390916609/'+str(ship.iloc[page-1,0])+'/'+str(ship.head().index[page-1])+'.png')
				await msg.edit(embed=embed)
			elif reaction.emoji=='▶️':
				if page!=len(ship):page+=1
				try:author=str(client.get_user(int(ship.iloc[page-1,1])))
				except:author='Unknown'
				if str(ship.iloc[page-1,4])=='nan':desc=''
				else:desc='\n'+str(ship.iloc[page-1,4])
				embed.description=index+' '+str(page)+'/'+str(len(ship))+'\n👍'+str(int(ship.iloc[page-1,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[page-1,2])+desc
				embed.set_image(url='https://cdn.discordapp.com/attachments/674632751390916609/'+str(ship.iloc[page-1,0])+'/'+str(ship.head().index[page-1])+'.png')
				await msg.edit(embed=embed)
			if hasattr(reaction.emoji,'id'):
				if reaction.emoji.id in [592757143892000769,592757119069978644]:
					if reaction.emoji.id==592757143892000769:#up
						buildpd.loc[ship.head().index[page-1],'Upvote']=str(buildpd.loc[ship.head().index[page-1],'Upvote']).replace(str(user.id)+'.','')+str(user.id)+'.'
						buildpd.loc[ship.head().index[page-1],'Downvote']=str(buildpd.loc[ship.head().index[page-1],'Downvote']).replace(str(user.id)+'.','')
					elif reaction.emoji.id==592757119069978644:#down
						buildpd.loc[ship.head().index[page-1],'Downvote']=str(buildpd.loc[ship.head().index[page-1],'Downvote']).replace(str(user.id)+'.','')+str(user.id)+'.'
						buildpd.loc[ship.head().index[page-1],'Upvote']=str(buildpd.loc[ship.head().index[page-1],'Upvote']).replace(str(user.id)+'.','')
					ship=buildpd.loc[buildpd.index.str.startswith(filename)]
					ship['Ratio']=[ 0.5 if row.Upvote.count('.')==0 and row.Downvote.count('.')==0 else row.Upvote.count('.')/(row.Upvote.count('.')+row.Downvote.count('.'))  for index, row in ship.iterrows() ]
					embed.description=index+' '+str(page)+'/'+str(len(ship))+'\n👍'+str(int(ship.iloc[0,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[0,2])+desc
					await msg.edit(embed=embed)
				elif reaction.emoji.id in [714760225466482689,714760495458156675,714760505797115905,714760514189787139,714760523027185794]:
					page=dict[reaction.emoji.id]
					try:author=str(client.get_user(int(ship.iloc[page-1,1])))
					except:author='Unknown'
					if str(ship.iloc[page-1,3])=='nan':desc=''
					else:desc='\n'+str(ship.iloc[page-1,3])
					embed.description=index+' '+str(page)+'/'+str(len(ship))+'\n👍'+str(int(ship.iloc[page-1,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[page-1,2])+desc
					embed.set_image(url='https://cdn.discordapp.com/attachments/674632751390916609/'+str(ship.iloc[page-1,0])+'/'+str(ship.head().index[page-1])+'.png')
					await msg.edit(embed=embed)
			await msg.remove_reaction(reaction,user) 
	#except:
	if False:
		embed.set_footer(text='')
		await msg.edit(embed=embed)
		await msg.clear_reactions()
		os.remove('build.csv')
		buildpd.to_csv('build.csv')
@client.command(aliases=(['i']))
async def index(ctx,*args):
	msg='Index:'		
	if len(args)==0:
		for index,row in buildcorrect[buildcorrect.Alternative.isnull()].iterrows():
			msg+='\n'+str(len(buildpd.loc[buildpd.index.str.startswith(row['Filename'])]))+'  '+str(index)
	else:
		for index in column(process.extractBests(ctx.message.content.replace('!index ','').replace('!i ',''),buildcorrect.index.values ,score_cutoff=50),0):
			msg+='\n'+str(len(buildpd.loc[buildpd.index.str.startswith(buildcorrect.loc[index,'Filename'])]))+'  '+str(index)
	await ctx.send(msg)
client.run(open("id.txt", "r").read())