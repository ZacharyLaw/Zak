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

ship=list(csv.reader(open("ship.csv","r")))
galaxy=list(csv.reader(open("galaxy.csv","r")))
build=list(csv.reader(open("build.csv","r")))
buildpd= pd.read_csv('build.csv', index_col=0)
generalpd= pd.read_csv('general.csv', index_col=0)
modulepd= pd.read_csv('module.csv', index_col=0)
cell=Image.open('cell.png')
client = discord.Client()
class MyClient(discord.Client):
	async def on_ready(self):
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
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
	async def on_raw_message_delete(self,payload):
		if not payload.cached_message.author.bot and not payload.cached_message.content.startswith('!') and payload.cached_message.guild.id==486870895978086400 and payload.cached_message.channel.id!=567848114170494976:
			msg=''
			channel = client.get_channel(670483927537811457)
			await channel.send(payload.cached_message.author.mention+':\n> '+payload.cached_message.content+'\nDeleted from '+payload.cached_message.channel.mention)
			if len(payload.cached_message.attachments)>0:
				opener=urllib.request.URLopener()
				opener.addheader('User-Agent', 'whatever')
				filename, headers = opener.retrieve(payload.cached_message.attachments[0].proxy_url,os.path.join('/home/zak/Zak/temp.png'))			
				await channel.send(file=discord.File('/home/zak/Zak/temp.png'))	
	async def on_message(self, message):
		roleid=[]
		for role in message.author.roles:roleid.append(role.id)
		#if message.content.includes('<@563319785811869698>'):await client.client_reaction("❤️")
		global usage,energy,width,height
		arg = message.content.split()
		if len(message.content.split(' '))>1:message.content=message.content.split('!')[0]+'!'+message.content.split('!')[1].split(' ')[0].lower()+' '+message.content.split(' ',1)[1]
		else:message.content=message.content.lower()
		#user = await bot.get_user_info("563319785811869698")
		"""
		elif message.content.startswith('!r') and message.author.id==27086497869854976:
		elif message.channel.id==620661949679665152 and message.content.startswith('delete my latest suggestion'):
			author_cache=str(message.author)
			await message.delete()
			channel = client.get_channel(567848114170494976)
			message=await channel.fetch_message(channel.last_message_id)
			message.content=str(message.content)
			if fuzz.partial_ratio(author_cache,message.content)==100:deleted = await channel.purge(limit=1)
		elif message.channel.id==620661949679665152 and not message.content.startswith('delete my latest suggestion'):
			await message.delete()
			channel = client.get_channel(567848114170494976)
			message=await channel.send(str(message.author)+':\n'+str(message.content))
			await message.add_reaction(client.get_emoji(592757143892000769))
			await message.add_reaction(client.get_emoji(592757119069978644))
		elif message.channel.id==581781769053798400:
			await message.delete()
			message=await message.channel.send(str(message.author)+':\n'+str(message.content))
			await message.add_reaction(client.get_emoji(592757143892000769))
			await message.add_reaction(client.get_emoji(592757119069978644))
		elif fuzz.partial_ratio('Bucky',message.mentions)==100 and fuzz.partial_ratio(message.content,'hug')==100:			
			await message.add_reaction('❤️')
		elif fuzz.partial_ratio('Bucky',message.mentions)==100 and fuzz.partial_ratio(message.content,'online?')==100:			
			#await message.add_reaction(client.get_emoji(524485045835137046))
			await message.add_reaction('👋')
		elif message.content.startswith('!kosupvotesugg'):
			approved=io.open("approved.txt","w", encoding="utf-8")
			async for message in client.get_channel(567848114170494976).history():
				for reaction in message.reactions:
					for user in await reaction.users().flatten():
						if user.id==557246731021058090 and str(reaction.emoji) == '<:upvote:592757143892000769>':
							approved.write('\n~~~~~~~~~~\n')
							approved.write(message.embeds[0].description)
			approved.close()
			await client.get_channel(528044464250552348).send(file=discord.File('C:\$Zac\spacearena\Zak\\approved.txt'))
		if message.channel.id==674247614501486620:
			await client.get_channel(486870895978086402).send(message.content)
			"""

		if message.author.id in [275813801792634880,234395307759108106,365975655608745985]:
			if message.author.id==275813801792634880 and message.channel.id!=567848114170494976 and message.channel.id!=551580844289032202:await message.delete()
			elif message.author.id==234395307759108106 and message.embeds[0].description.startswith('Groovy is the easiest way'):await message.delete()
			elif message.author.id==234395307759108106 and message.embeds[0].description.startswith('You must be playing a track to use this command!'):await message.delete()
			elif message.author.id==365975655608745985 and message.embeds[0].title.startswith('Congratulations'):await message.delete()
		if message.channel.id == 620661949679665152: await message.delete()
		if message.author.id == self.user.id or not (message.content.startswith('!') or message.content.startswith('+') or message.content.startswith('-')):return
		elif message.content.startswith('!w '):
			arg[0]=''
			embed = discord.Embed()
			embed.add_field(name='Wikia Search result:',value='['+' '.join(map(str, wikia.search('spacearena',' '.join(map(str, arg)),1)))+'](http://spacearena.fandom.com/wiki/'+' '.join(map(str, wikia.search('spacearena',' '.join(map(str, arg)),1))).replace(' ','_')+')')
			await message.channel.send(embed=embed)
		elif message.content.lower()=='!zak':await message.add_reaction('👋')
		elif message.content.lower()=='!fact':
			await message.channel.send( ' '.join(random.choice(list(csv.reader(open("fact.txt","r"))))))
		elif message.content.startswith('!invite'):
			embed = discord.Embed()
			embed.add_field(name="Bucky Invite Link", value='[link](https://discordapp.com/oauth2/authorize?client_id=563319785811869698&scope=bot)')
			await message.channel.send(embed=embed)
		elif message.content.startswith('what') and 'pdt' in message.content:
			await message.channel.send('<:pdt:563962230278848522> Point Defense Turret')
		elif message.content.startswith('!about'):
			embed = discord.Embed(description='<@563319785811869698> is made by <@270864978569854976>\nFor the Space Arena Offical Server\nBorn at 10/12/2019\nNice to meet you Senpi!\n[Github](http://github.com/ZacharyLaw/Zak)',colour=discord.Colour.from_rgb(47,49,54))
			await message.channel.send(embed=embed)
			#await message.channel.send('<@563319785811869698> is made by <@270864978569854976>\nFor the Space Arena Offical Server\nBorn at 10/12/2019\nNice to meet you Senpi!')
		elif message.content.startswith('!sector'):
			data=list(csv.reader(open("sector.csv","r")))
			await message.channel.send('Sector '+str(arg[1])+'.'+str(arg[2])+' '+data[(int(arg[1])-1)*10+int(arg[2])-1][5]+'\n<:ballistic:570222613180186653>'+data[(int(arg[1])-1)*10+int(arg[2])-1][0]+'/19\n<:missile:570222563779936256>'+data[(int(arg[1])-1)*10+int(arg[2])-1][1]+'/19\n<:laser:570222555802107905>'+data[(int(arg[1])-1)*10+int(arg[2])-1][2]+'/19\n<a:armor:654546483613270017>'+data[(int(arg[1])-1)*10+int(arg[2])-1][3]+'/19\n<a:shield:654546575858860043>'+data[(int(arg[1])-1)*10+int(arg[2])-1][4]+'/19')
		#elif message.content.startswith('!guide') or message.content.startswith('!zac'):await message.channel.send(file=discord.File('/home/zak/Zak/guide.gif'))
		elif message.content.startswith('!guide') or message.content.startswith('!zac'):await message.channel.send('https://cdn.discordapp.com/attachments/566268214514941952/684388364337676516/guide.gif')
		elif message.content.startswith('!stonk'):await message.channel.send(file=discord.File('/home/zak/Zak/stonk.png'))
		elif message.content.startswith('!weap') or message.content.startswith('!weapon'):await message.channel.send(file=discord.File('/home/zak/Zak/weap.png'))
		elif message.content.startswith('!upg') or message.content.startswith('!upgrade'):await message.channel.send(file=discord.File(r'/home/zak/Zak/upg6.png'))
		elif message.content.startswith('!cou'):
			await message.channel.send(file=discord.File('/home/zak/Zak/counter4.png'))
		elif message.content.startswith('!bb'):await message.channel.send(file=discord.File('/home/zak/Zak/bb.png'))
		elif message.content.startswith('!combo'):
			await message.channel.send(file=discord.File('/home/zak/Zak/combo.png'))
		elif message.content.startswith('!shipupg'):
			await message.channel.send(file=discord.File('/home/zak/Zak/shipupg3.png'))
		elif message.content in ['!ship','!ships']:#/home/zak/Zak/ /home/zak/Zak/
			await message.channel.send(file=discord.File('/home/zak/Zak/ship.png'))
		elif message.content.startswith('!mod'):await message.channel.send(file=discord.File('/home/zak/Zak/mod.png'))
		elif message.content.startswith('!event') or message.content.startswith('!grind'):
			def dateDiffInSeconds(date1, date2):
				timedelta = date2 - date1
				return timedelta.days * 24 * 3600 + timedelta.seconds
			def daysHoursMinutesSecondsFromSeconds(seconds):
				minutes, seconds = divmod(seconds, 60)
				hours, minutes = divmod(minutes, 60)
				days, hours = divmod(hours, 24)
				return (days, hours, minutes)
			leaving_date = datetime.strptime('2020-02-24 07:55:00', '%Y-%m-%d %H:%M:%S')
			now = datetime.now()
			await message.channel.send ("Event countdown %dd %dh %dm" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, leaving_date)))
		elif message.content.startswith('!time'):
			def HoursMinutesFromSeconds():
				seconds=(datetime.strptime('11:00:00','%H:%M:%S')-datetime.now()).seconds
				minutes, seconds = divmod(seconds, 60)
				hours, minutes = divmod(minutes, 60)
				return (hours, minutes)
			targetday = date.today()
			while targetday.weekday() != 0:
				targetday += timedelta(1)
			target=datetime.combine(targetday,datetime.strptime('1000','%H%M').time())
			def DaysHoursMinutesFromSeconds():
				seconds=((target-datetime.now()).days)*86400
				seconds+=(target-datetime.now()).seconds
				days, seconds = divmod(seconds, 24*60*60)
				hours, seconds = divmod(seconds, 60*60)
				minutes, seconds = divmod(seconds, 60)
				return (days, hours, minutes)
			await message.channel.send('Daily quest & Daily Deals countdown: %dh %dm\n'% HoursMinutesFromSeconds() +'Class Battle countdown: %dd %dh %dm\n' % DaysHoursMinutesFromSeconds()+'HeroCraft HQ Time: '+(datetime.today()+timedelta(hours=2)).strftime("%H:%M"))
		elif message.content.startswith('!daily'):
			def HoursMinutesSecondsFromSeconds():
				seconds=(datetime.strptime('19:00:00','%H:%M:%S')-datetime.now()).seconds
				minutes, seconds = divmod(seconds, 60)
				hours, minutes = divmod(minutes, 60)
				return (hours, minutes)
			await message.channel.send("Daily quest countdown: %dh %dm" % HoursMinutesSecondsFromSeconds())
		elif message.content.startswith('!cb'):
			targetday = date.today()
			while targetday.weekday() != 0:
				targetday += timedelta(1)
			target=datetime.combine(targetday,datetime.strptime('1000','%H%M').time())
			def DaysHoursMinutesSecondsFromSeconds():
				seconds=((target-datetime.now()).days)*86400
				seconds+=(target-datetime.now()).seconds
				days, seconds = divmod(seconds, 24*60*60)
				hours, seconds = divmod(seconds, 60*60)
				minutes, seconds = divmod(seconds, 60)
				return (days, hours, minutes)
			await message.channel.send('Class Battle countdown: %dd %dh %dm' % DaysHoursMinutesSecondsFromSeconds())
		elif message.content.startswith('!explore ') or message.content.startswith('!galaxy ') or message.content == '!g' or message.content == '!e':
			if len(arg)==3:
				if message.channel.id==528044464250552348 or message.channel.id==655982019209330699:
					if int(arg[2])>100:repeat = 100
					else: repeat = int(arg[2])
			else:repeat=1
			for i in range(repeat):
				msg=''
				if len(arg)==1:await message.channel.send('Galaxy explore simulator\nAll galaxy only in L9 reward pool, not fully accurate\nAvaliable galaxy:\n`alpha` or `a`\n`epsilon` or `e`\n`zeta` or `z`\n`iota` or `i`\n`beta` or `b`\n`delta` or `d`\n`theta` or `t`')
				elif arg[1]=='alpha'or arg[1]=='a':#0 1 2
					rand=random.randrange(len(galaxy[0])-galaxy[0].count(''))
					if random.getrandbits(1):msg=random.choice([str(random.randint(1,3))+' Chip<:chip:570222029521813534>\n','1 Overclock Chip<:oc:570222019770187776>\n'])
					if random.getrandbits(1):msg+=str(random.choice(['1 Modify Chance Lv','1 Increase Chance Lv','1 Chip Reduction Lv','1 Credit Reduction Lv']))+str(random.randint(2,5))+'\n'
					await message.channel.send('Opened L9 Alpha<:alpha:654592161161150485>\n'+str(random.randrange(2200,43200))+'<:credit:570222178348564481>\n'+str(random.randint(1,3))+str(random.choice([' Modify Chance Lv1\n',' Increase Chance Lv1\n',' Chip Reduction Lv1\n',' Credit Reduction Lv1\n']))+msg+str(random.randrange(int(galaxy[1][rand]),int(galaxy[2][rand])+1))+' '+str(galaxy[0][rand])+' <:blueprint:568688146683002880>')
				elif arg[1]=='epsilon'or arg[1]=='e':#3 4 5
					rand=random.randrange(len(galaxy[0])-galaxy[3].count(''))
					if random.getrandbits(1):msg='\n'+random.choice([str(random.randint(1,3))+' Chip <:chip:570222029521813534>','1 Overclock Chip<:oc:570222019770187776>'])
					if random.getrandbits(1):msg+=str(random.choice(['\n1 Modify Chance Lv','\n1 Increase Chance Lv','\n1 Chip Reduction Lv','\n1 Credit Reduction Lv']))+str(random.randint(3,5))
					await message.channel.send('Opened L9 Epsilon<:epsilon:649520458932158474>\n'+str(random.randrange(6260,56700))+'<:credit:570222178348564481>\n'+str(random.randint(1,3))+str(random.choice([' Modify Chance Lv',' Increase Chance Lv',' Chip Reduction Lv',' Credit Reduction Lv']))+str(random.randint(1,2))+msg+'\n'+str(random.randrange(int(galaxy[4][rand]),int(galaxy[5][rand])+1))+' '+str(galaxy[3][rand])+' <:blueprint:568688146683002880>')
				elif arg[1]=='zeta'or arg[1]=='z':#6 7 8
					rand=random.randrange(len(galaxy[0])-galaxy[6].count(''))
					if random.randint(1,3)==3:msg=str(random.choice(['1 Modify Chance Lv3','1 Increase Chance Lv3','1 Chip Reduction Lv3','1 Credit Reduction Lv3']))
					else:msg=str(random.randint(1,3))+str(random.choice([' Modify Chance Lv2',' Increase Chance Lv2',' Chip Reduction Lv2',' Credit Reduction Lv2']))
					if random.getrandbits(1):msg+='\n'+random.choice([str(random.randint(1,4))+' Chip<:chip:570222029521813534>',str(random.randint(1,2))+' Overclock Chip<:oc:570222019770187776>'])
					if random.getrandbits(1):msg+=str(random.choice(['\n1 Modify Chance Lv','\n1 Increase Chance Lv','\n1 Chip Reduction Lv','\n1 Credit Reduction Lv']))+str(random.randint(4,5))
					await message.channel.send('Opened L9 Zeta<:zeta:649514690057076736>\n'+str(random.randrange(9010,82000))+'<:credit:570222178348564481>\n'+msg+'\n'+str(random.randrange(int(galaxy[7][rand]),int(galaxy[8][rand])+1))+' '+str(galaxy[6][rand])+' <:blueprint:568688146683002880>')
				elif arg[1]=='iota'or arg[1]=='i':#9 10 11
					rand=random.randrange(len(galaxy[0])-galaxy[9].count(''))
					if random.getrandbits(1):msg+=random.choice([str(random.randint(1,4))+' Chip<:chip:570222029521813534>\n',str(random.randint(1,2))+' Overclock Chip<:oc:570222019770187776>\n'])
					await message.channel.send('Opened L9 Iota<:iota:649858869689974794>\n'+str(random.randrange(81630,1476200))+'<:credit:570222178348564481>\n'+msg+str(random.randint(1,3))+str(random.choice([' Modify Chance Lv3\n',' Increase Chance Lv3\n',' Chip Reduction Lv3\n',' Credit Reduction Lv3\n']))+str(random.choice(['1 Modify Chance Lv','1 Increase Chance Lv','1 Chip Reduction Lv','1 Credit Reduction Lv']))+str(random.randint(4,5))+'\n'+str(random.randrange(int(galaxy[10][rand]),int(galaxy[11][rand])+1))+' '+str(galaxy[9][rand])+' <:blueprint:568688146683002880>')
				elif arg[1]=='beta'or arg[1]=='b':#12 13 14
					rand=random.randrange(len(galaxy[0])-galaxy[12].count(''))
					if random.getrandbits(1):msg=str(random.randint(1,10))+' Random <:blueprint:568688146683002880> matches your shipyard'
					await message.channel.send('Opened L9 Beta<a:beta:654597450149003294>\n'+str(random.randrange(int(galaxy[13][rand]),int(galaxy[14][rand])+1))+' '+str(galaxy[12][rand])+' <:blueprint:568688146683002880>\n'+msg)
				elif arg[1]=='delta'or arg[1]=='d':#15 16 17
					rand=random.randrange(len(galaxy[0])-galaxy[15].count(''))
					await message.channel.send('Opened L9 Delta<a:delta:654597441756332043>\n'+str(random.randrange(int(galaxy[16][rand]),int(galaxy[17][rand])+1))+' '+str(galaxy[15][rand])+' <:blueprint:568688146683002880>')
				elif arg[1]=='theta'or arg[1]=='t':#18 19 20
					rand=random.randrange(len(galaxy[0])-galaxy[18].count(''))
					await message.channel.send('Opened L9 Theta<a:theta:654597424844898315>\n'+str(random.randrange(int(galaxy[19][rand]),int(galaxy[20][rand])+1))+' '+str(galaxy[18][rand])+' <:blueprint:568688146683002880>')
				await asyncio.sleep(3.0)
		
		elif message.content.startswith('!cell'):
			if arg[1]=='pss':arg.pop(1)
			if arg[1]=='sparrow':
				await message.channel.send(file=discord.File('/home/zak/Zak/cell/psssparrow.png'))
			elif arg[1]=='wing':
				await message.channel.send(file=discord.File('/home/zak/Zak/cell/wing.png'))
			elif process.extractOne(arg[1],buildpd.index.values ,score_cutoff=80):
				await message.channel.send(file=discord.File('/home/zak/Zak/cell/'+str(buildpd.loc[process.extractOne(arg[1],buildpd.index.values ,score_cutoff=80)[0],'Filename'])+'.png'))
		elif message.content.startswith('!cost'):
			message.content=message.content.replace('mkiii','mk3').replace('mkii','mk2')
			index=''.join(map(str,process.extractOne(message.content.split('!cost',1)[1],generalpd.index.values,score_cutoff=80)[0])) 
			if str(generalpd.loc[index,'Alternative'])!='nan': index=str(generalpd.loc[index,'Alternative'])
			msg=str(index)+'\n'
			if str(generalpd.loc[index,'Acquisition'])!='nan':msg+='Acquisition: '+str(generalpd.loc[index,'Acquisition'])
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])=='nan' and str(generalpd.loc[index,'Blueprint'])=='nan':msg+='Cost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])!='nan':msg+='Cost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481> / '+str(generalpd.loc[index,'Celestium'])+'<:celes:570222210476670976>'
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Blueprint'])!='nan':msg+='Cost: '+str(int(generalpd.loc[index,'Blueprint']))+'<:blueprint:568688146683002880> & '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
			await message.channel.send(msg)		
		elif message.content.startswith('!unlock'):
			message.content=message.content.replace('mkiii','mk3').replace('mkii','mk2')
			index=''.join(map(str,process.extractOne(message.content.split('!unlock',1)[1],generalpd.index.values,score_cutoff=80)[0])) 
			if str(generalpd.loc[index,'Alternative'])!='nan': index=str(generalpd.loc[index,'Alternative'])
			await message.channel.send(str(index)+'\nLevel: '+str(int(generalpd.loc[index,'Level'])))
		elif message.content.startswith('!meme'):
			await message.channel.send(file=discord.File('/home/zak/Zak/meme/meme'+str(random.randint(1,58))+'.png'))
		elif message.content.startswith('!info '):
			message.content=message.content.replace('mkiii','mk3').replace('mkii','mk2')
			index=''.join(map(str,process.extractOne(message.content.split('!info',1)[1],generalpd.index.values,score_cutoff=80)[0])) 
			if str(generalpd.loc[index,'Alternative'])!='nan': index=str(generalpd.loc[index,'Alternative'])
			page1=str(index)+' <a:one1:664298489018318858>\nLevel: '+str(generalpd.loc[index,'Level'])
			if str(generalpd.loc[index,'Acquisition'])!='nan':msg='\nAcquisition: '+str(generalpd.loc[index,'Acquisition'])
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])=='nan' and str(generalpd.loc[index,'Blueprint'])=='nan':page1+='\nCost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Celestium'])!='nan':page1+='\nCost: '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481> / '+str(generalpd.loc[index,'Celestium'])+'<:celes:570222210476670976>'
			elif str(generalpd.loc[index,'Credit'])!='nan' and str(generalpd.loc[index,'Blueprint'])!='nan':page1+='\nCost: '+str(int(generalpd.loc[index,'Blueprint']))+'<:blueprint:568688146683002880> & '+str(generalpd.loc[index,'Credit'])+'<:credit:570222178348564481>'
			page2=str(index)+' <a:two2:664298764437028886>'
			for title in ['Speed','Turning','Cell','Max','Support','Supp. Cell','Supp. Max','Size','Power Use','Health','Armor','Mass','Reflect']:
				if str(generalpd.loc[index,title])!='nan':
					try:page2+='\n'+title+': '+str(int(generalpd.loc[index,title]))
					except:page2+='\n'+title+': '+str(generalpd.loc[index,title])
			page3=str(index)+' <a:three3:664298774264283149>'
			for title in ['Mod 1','Mod 2','Mod 3','Mod 4','Mod 5','Supp. Mod 1','Supp. Mod 2','Supp. Mod 3','Supp. Mod 4','Supp. Mod 5','Anti Penetration Damage','Power Generation','Explosion Damage','Explosion Radius','Damage','Range','Fire Cone','Fire Rate','Penetrating Damage','No. of Missiles','Rocket Explosion Radius','Flight Time','No. of Mines','Mines Explosion Radius','Mine Lifespan','Laser Duration','Max Regeneration','Regen Speed','Shield Radius','Shield Strength','Junk Amount','Junk Flight Time','Mine Disruption %','Rocket Disruption %','Torpedo Disruption %','Thrust Power','Warp Force','Duration','Thrust Boost','Turning Boost','Max Module']:
				if str(generalpd.loc[index,title])!='nan':page3+='\n'+title+': '+str(generalpd.loc[index,title])
			page4=str(index)+' <a:four4:664298786323038242>'
			if str(generalpd.loc[index,'Upgradeable Bonus'])!='nan':page4+='\nUpgradeable Bonus:\n'+str(generalpd.loc[index,'Upgradeable Bonus'])
			if str(generalpd.loc[index,'Unique Bonus'])!='nan':page4+='\nUnique Bonus: '+str(generalpd.loc[index,'Unique Bonus'])
			message=await message.channel.send(page1)
			if '\n' in page1: await message.add_reaction('<a:one1:664298489018318858>')
			if '\n' in page2: await message.add_reaction('<a:two2:664298764437028886>')
			if '\n' in page3: await message.add_reaction('<a:three3:664298774264283149>')
			if '\n' in page4: await message.add_reaction('<a:four4:664298786323038242>')
			def check(reaction,user):return user.id!=563319785811869698
			end = time.time() + 60
			try:
				while time.time() < end:
					reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
					if reaction.message.id==message.id:
						if reaction.emoji.id==664298489018318858 and '\n' in page1:await message.edit(content=page1)
						elif reaction.emoji.id==664298764437028886 and '\n' in page2:await message.edit(content=page2)
						elif reaction.emoji.id==664298774264283149 and '\n' in page3:await message.edit(content=page3)
						elif reaction.emoji.id==664298786323038242 and '\n' in page4:await message.edit(content=page4)
					await message.remove_reaction(reaction,user)
				await message.clear_reactions()
			except:await message.clear_reactions()
					
		elif message.content.startswith('!power ') or message.content.startswith('!energy '):
			message.content=message.content.replace('mkiii','mk3').replace('mkii','mk2')
			content=message.content.split(' ', 1)[1]
			usage=0
			energy=0
			for spliter in content.split(','):
				if spliter[0]==' ':spliter=spliter[1:]
				amount=spliter.split(' ', 1)[0]
				item=''.join(map(str,process.extractOne(spliter.split(' ', 1)[1],generalpd.index.values,score_cutoff=80)[0])) 
				if str(generalpd.loc[item,'Alternative'])!='nan': item=str(generalpd.loc[item,'Alternative'])
				if str(generalpd.loc[item,'Power Use'])!='nan':usage+=int(generalpd.loc[item,'Power Use'])*int(amount)
				elif str(generalpd.loc[item,'Power Generation'])!='nan':energy+=int(generalpd.loc[item,'Power Generation'])*int(amount)
				try:
					if int(energy/usage)*100>100:percent='100%: '
					else:percent=str(int(energy/usage*100))+'%: '
				except:percent='100%: '
			await message.channel.send(percent+str(usage)+'/'+str(energy))   
		elif message.content.startswith('!shop'):
			if message.content=='!shop':await message.channel.send('`!shpp [item] [quanity] [price]celes [image link]`\nEg : `!shop Infinity Gauntlet x1 999celes http:// ... .png')
			else:
				urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
				price=quanity=msg=' '
				for word in message.content.split(' '):
					if 'celes' in word:price=word.split('celes')[0]
					elif 'x' in word[0]:quanity=word
				msg=message.content.split('!shop')[1].split(quanity)[0]
				if price==' ' or quanity==' ' or msg==' ':await message.channel.send('Missing arguement(s)\n`!shpp [item] [quanity] [price]celes [image link]`\nEg : `!shop Infinity Gauntlet x1 999celes http:// ... .png`')
				elif len(urls)==0:await message.channel.send('No image recieved')
				else:
					preshop = Image.open("preshop.png")
					opener=urllib.request.URLopener()
					opener.addheader('User-Agent', 'Something')
					filename, headers = opener.retrieve(urls[0],os.path.join('item.png'))
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
					await message.channel.send(file=discord.File('shop.png'))
		elif message.content.startswith('!update') and (message.author.guild_permissions.administrator or message.author.id==270864978569854976 or 577707621193351188 in roleid):
			urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
			msg=''
			if len(arg)==1:msg+='Error: One word only\n'
			elif not arg[1] in ['ship.png','weap.png','module.csv','general.csv','build.csv']:msg+='Error: Not provide/wrong filename\n'
			if not (len(urls)==1 or len(message.attachments)==1):msg+='Error: Not provide attachment/url\n'
			if len(urls)==1 and len(message.attachments)==1:msg+='Error: Only accept either attachment/url\n'
			if len(urls)==0 and len(message.attachments)==1:urls.append(message.attachments[0].url)
			if len(arg)>1 and ((arg[1] in ['ship.png','weap.png'] and not ('.png' in urls[0] or '.jpg' in urls[0])) or (arg[1] in ['module.csv','general.csv','build.csv'] and not ('.csv' in urls[0] or '.xlsx' in urls[0]))):msg+='Error: Wrong filetype\n'
			if msg!='':await message.channel.send(content=msg+'Admininistrator permission owner only command: Update file\n`!update [file] [link/attachment]`\nFile: `ship.png`, `weap.png`, `general.csv`, `module.csv`, `build.csv`\nEg: `!update ship.png http://www... .png`\nAccept png/jpg/csv/xlsx accordingly',files=[discord.File('ship.png'),discord.File('weap.png'),discord.File('general.csv'),discord.File('module.csv'),discord.File('build.csv')])
			else:
				opener=urllib.request.URLopener()
				opener.addheader('User-Agent', 'Something')
				filename, headers = opener.retrieve(urls[0],os.path.join(arg[1]))
				await message.add_reaction('✅')
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
client = MyClient()
client.run(open("id.txt", "r").read())
