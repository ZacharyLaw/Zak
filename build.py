import discord
import csv
from fuzzywuzzy import process,fuzz
import glob
import pandas as pd
import os
import numpy as np
import sys
import re
import requests
from PIL import Image
import shutil
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
def column(matrix, i):
	return [row[i] for row in matrix]
build=pd.read_csv('build.csv', index_col=0,dtype=str).fillna('')
buildcorrect= pd.read_csv('buildcorrect.csv', index_col=0)
dict={714760225466482689:1,714760495458156675:2,714760505797115905:3,714760514189787139:4,714760523027185794:5}
react={1:'1one:714760225466482689',2:'2two:714760495458156675',3:'3three:714760505797115905',4:'4four:714760514189787139',5:'5five:714760523027185794',6:'6six:714769193517449257'}
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
		global botchannel
		botchannel=client.get_channel(674632751390916609)
	async def on_message(self, message):
		arg = message.content.split()
		if message.author.id == self.user.id or not (message.content.startswith('!') or message.content.startswith('+') or message.content.startswith('-')):pass		
		elif message.content.startswith('!submit'):
			sender=message
			try:
				if re.findall('https://ptb.discordapp.com/channels/\d+/\d+/\d+',message.content):
					msglink=re.findall('https://ptb.discordapp.com/channels/\d+/\d+/\d+',message.content)[0]
					message=await client.get_channel(int(msglink.split('/')[5])).fetch_message(int(msglink.split('/')[6]))
					shipname=re.sub(r"http\S+", "", sender.content.replace('!submitbuild' ,'',1).replace('!submit' ,'',1))
					desc='\n'+message.content
				else:
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
					if ',' in message.content:shipname=re.sub(r"http\S+", "",  message.content.replace('!submitbuild' ,'',1).replace('!submit' ,'',1).split(',',1)[0])
					elif ',' not in message.content:shipname=re.sub(r"http\S+", "",  message.content.replace('!submitbuild' ,'',1).replace('!submit' ,'',1))				
					if ',' not in message.content:desc=''
					else:desc=re.sub(r"http\S+", "",  message.content.split(',',1)[1])			
				urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
				if len(message.attachments)==0 and len(urls)==0:await sender.channel.send('No image recieved')
				elif shipname=='':await sender.channel.send('No shipname received')
				elif not (process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80) or process.extractOne(shipname,buildcorrect.index.values ,score_cutoff=80)):await sender.channel.send('Shipname not found')
				else:
					if len(urls)==0 and len(message.attachments)==2:urls=[message.attachments[0].url,message.attachments[1].url]
					elif len(urls)==0 and len(message.attachments)==1:urls=[message.attachments[0].url]
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
						if not filename+str(x+1) in build.index:
							filename=filename+str(x+1)+'.png'
							break
					open(filename, 'wb').write(requests.get(urls[0]).content)
					if len(urls)==2:
						open('temp.png', 'wb').write(requests.get(urls[1]).content)
						horizontal_resize_merge(filename, 'temp.png',filename)
					screenshot=await botchannel.send(file=discord.File(filename))
					os.remove(filename)
					desc2='\n' if desc=='' else ''+desc
					embed = discord.Embed(description=index+'\nAuthor: '+str(message.author)+'\n'+str(message.created_at.strftime("%d/%m/%Y"))+desc2,colour=discord.Colour.from_rgb(47,49,54))
					embed.set_image(url=screenshot.attachments[0].url)
					embed.set_footer(text='✅ To Confirm',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
					try:
						confirm=await sender.channel.send(embed=embed)
						def check(reaction,user):return user == sender.author and reaction.emoji=='✅'
						await confirm.add_reaction('✅')
						reaction,user = await client.wait_for('reaction_add',check=check,timeout=60.0)
						build.loc[filename.replace('.png','')]=[str(screenshot.attachments[0].id),str(message.author.id),str(message.created_at.strftime("%d/%m/%Y")),desc,'','']
						os.remove('build.csv')
						build.to_csv('build.csv')
						embed.set_footer(text='Submitted')
						await confirm.edit(embed=embed)
						await confirm.clear_reactions()
					except:
						embed.set_footer(text='Failed Submit')
						await confirm.edit(embed=embed)
						await confirm.clear_reactions()
			except discord.errors.Forbidden:await sender.channel.send('Missing permission')
		elif message.content.startswith('!build') or message.content.startswith('!b '):
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
			ship=build.loc[build.index.str.startswith(filename)]
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
			def check(reaction,user):return user != self.user and reaction.message.id==msg.id
			try:
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
								build.loc[ship.head().index[page-1],'Upvote']=str(build.loc[ship.head().index[page-1],'Upvote']).replace(str(user.id)+'.','')+str(user.id)+'.'
								build.loc[ship.head().index[page-1],'Downvote']=str(build.loc[ship.head().index[page-1],'Downvote']).replace(str(user.id)+'.','')
							elif reaction.emoji.id==592757119069978644:#down
								build.loc[ship.head().index[page-1],'Downvote']=str(build.loc[ship.head().index[page-1],'Downvote']).replace(str(user.id)+'.','')+str(user.id)+'.'
								build.loc[ship.head().index[page-1],'Upvote']=str(build.loc[ship.head().index[page-1],'Upvote']).replace(str(user.id)+'.','')
							ship=build.filter(like=filename,axis=0)
							ship['Ratio']=[ 0.5 if row.Upvote.count('.')==0 and row.Downvote.count('.')==0 else row.Upvote.count('.')/(row.Upvote.count('.')+row.Downvote.count('.'))  for index, row in ship.iterrows() ]
							embed.description=index+' 1/'+str(len(ship))+'\n👍'+str(int(ship.iloc[0,6]*100))+'%\nAuthor: '+author+'\n'+str(ship.iloc[0,2])+desc
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
			except:
				embed.set_footer(text='')
				await msg.edit(embed=embed)
				await msg.clear_reactions()
				os.remove('build.csv')
				build.to_csv('build.csv')
		elif message.content.startswith('!cell'):
			await message.channel.send(file=discord.File('/home/zak/Zak/cell/'+str(buildcorrect.loc[str(process.extractOne(message.content.replace('!cell',''),buildcorrect.index.values ,score_cutoff=80)[0]),'Filename'])+'.png'))
		elif message.content.startswith('!index') or message.content.startswith('!i '):
			msg='Index:'		
			if len(arg)==1:
				for index,row in buildcorrect[buildcorrect.Alternative.isnull()].iterrows():
					msg+='\n'+str(len(build.loc[build.index.str.startswith(row['Filename'])]))+'  '+str(index)
			else:
				for index in column(process.extractBests(message.content.replace('!index ','').replace('!i ',''),buildcorrect.index.values ,score_cutoff=50),0):
					msg+='\n'+str(len(build.loc[build.index.str.startswith(buildcorrect.loc[index,'Filename'])]))+'  '+str(index)
			await message.channel.send(msg)
client = MyClient()
client.run(open("id.txt", "r").read())