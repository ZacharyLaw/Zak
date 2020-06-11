import discord
import asyncio
import csv
from fuzzywuzzy import process,fuzz
import pandas as pd
import os
from PIL import Image
import pathlib
#py -m pip 
generalpd= pd.read_csv('general.csv', index_col=0)
modulepd= pd.read_csv('module.csv', index_col=0)
cell=Image.open('cell.png')
cursor=Image.open('cursor.png').convert("RGBA")
null=Image.new('RGB', (100,100))
null.putalpha(0)
cell=Image.open('cell.png')
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
client = discord.Client()
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
		global botchannel
		botchannel=client.get_channel(674632751390916609)
	async def on_message(self, message):
		message.content = message.content.lower()
		global usage,energy,width,height
		if message.author.id == self.user.id or not (message.content.startswith('!') or message.content.startswith('+')):return
		elif message.content.startswith('!creator'):
			xcoord=ycoord=1
			image = Image.new('RGB', (100,100))
			image.putalpha(0)
			image.save('create.png')
			image.paste(cursor,(0,0),mask=cursor)
			image.save('cursored.png')
			channel=message.channel
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
			#await creator.add_reaction('<:engine:690840753298997278>')#engine
			#await creator.add_reaction('<:modification:559571165945921558>')#mod
			hide=usage=energy=lock=0
			try:
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
			except:await creator.clear_reactions()			
client = MyClient()
client.run(open("id.txt", "r").read())
