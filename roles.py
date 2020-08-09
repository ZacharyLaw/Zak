import discord
import asyncio
import os
#py -m pip 
async def add1(channel,message,member,payload):
	if unverified in member.roles:
		await member.remove_roles(unverified)
		await gen_ch.send('Welcome '+member.mention+'.\nYou may introduce yourself in <#575503557701271553> so we get to know you better! If you are in the top 100 or are a content creator for Space Arena, message a Jedi master (moderator) for your special role')
		await log_ch.send('Verified '+member.mention)
async def add2(channel,message,member,payload):
	if message.content.startswith('__***Rules & Important***__'):
		if payload.emoji.name in ['android','ios','pc']:await member.add_roles(dictionary[payload.emoji.name])
		else:await message.remove_reaction(payload.emoji,member)
async def add3(channel,message,member,payload):
	if message.content.startswith('Your top ship class:'):
		for role in member.roles:
			try:await member.remove_roles(dictionary[role.name.lower().replace(' ','')])
			except:pass
		await member.add_roles(dictionary[payload.emoji.name])
		await message.remove_reaction(payload.emoji,member)
async def add4(channel,message,member,payload):
	if message.content.startswith('Press '):
		if payload.emoji.name =='ru':await member.add_roles(ru)
		else:await message.remove_reaction(payload.emoji,member)
client = discord.Client()
class MyClient(discord.Client):
	async def on_ready(self):
		global guild,dictionary,unverified,android,ios,pc,ru,log_ch,gen_ch,corvette,frigate,cruiser,battleship,carrier,suppercarrier,galacticcarrier
		guild=discord.utils.find(lambda g: g.id == 486870895978086400, client.guilds)
		dictionary={'corvette':guild.get_role(515173171742244884)
		,'frigate':guild.get_role(506117736070381578)
		,'cruiser':guild.get_role(487742396914991114)
		,'battleship':guild.get_role(487947882238967820)
		,'carrier':guild.get_role(496090951056621591)
		,'suppercarrier':guild.get_role(487052478760747019)
		,'galacticcarrier':guild.get_role(632508763844116490)
		,'android':guild.get_role(517175120431808523)
		,'ios':guild.get_role(515299388080390145)
		,'pc':guild.get_role(558226800296329216)
		,'ru':guild.get_role(657521436113764352)}
		unverified=guild.get_role(638594355661373460)
		log_ch=client.get_channel(570348053051998253)
		gen_ch=client.get_channel(486870895978086402)
		corvette=guild.get_role(515173171742244884)
		frigate=guild.get_role(506117736070381578)
		cruiser=guild.get_role(487742396914991114)
		battleship=guild.get_role(487947882238967820)
		carrier=guild.get_role(496090951056621591)
		suppercarrier=guild.get_role(487052478760747019)
		galacticcarrier=guild.get_role(632508763844116490)
		android=guild.get_role(517175120431808523)
		ios=guild.get_role(515299388080390145)
		pc=guild.get_role(558226800296329216)
		ru=guild.get_role(657521436113764352)
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
	async def on_raw_reaction_add(self,payload):
		channel = client.get_channel(payload.channel_id)
		message=await channel.fetch_message(payload.message_id)
		member= guild.get_member(payload.user_id)
		if channel.guild== guild and member.id!=563319785811869698 and channel.name.startswith('rules'):await asyncio.gather(add1(channel,message,member,payload),add2(channel,message,member,payload),add3(channel,message,member,payload),add4(channel,message,member,payload))
	async def on_raw_reaction_remove(self,payload):
		channel = client.get_channel(payload.channel_id)
		message=await channel.fetch_message(payload.message_id)
		member= guild.get_member(payload.user_id)
		if channel.guild==guild and message.content.startswith('__***Rules & Important***__') and member.id!=563319785811869698 and channel.name.startswith('rules') and (len(member.roles)>2 or not member.top_role.id in [517175120431808523,515299388080390145,558226800296329216]):
			await member.remove_roles(dictionary[payload.emoji.name])
		elif channel.guild== guild and message.content.startswith('Press ') and member.id!=563319785811869698 and channel.name.startswith('rules') and payload.emoji.name=='ru' and  (len(member.roles)>2 or member.top_role.id!=657521436113764352):
			await member.remove_roles(ru)
	async def on_message(self, message):
		if message.content.startswith('Your top ship class:') and message.channel.name.startswith('rules') and channel.guild== guild:
			await message.add_reaction('<a:corvette:648546484425326612>')
			await message.add_reaction('<a:frigate:648546513772871691>')
			await message.add_reaction('<a:cruiser:648546497092255754>')
			await message.add_reaction('<a:battleship:648546462816272415>')
			await message.add_reaction('<a:carrier:648546474749329410>')
			await message.add_reaction('<a:supercarrier:648546541061275658>')
			await message.add_reaction('<a:galacticcarrier:648546526360240140>')
		elif message.content.startswith('__***Rules & Important***__') and message.channel.name.startswith('rules') and channel.guild== guild:
			await message.add_reaction('<a:android:648546422383312906>')
			await message.add_reaction('<a:ios:648546440053915688>')
			await message.add_reaction('<a:pc:648546451777126412>')
		elif message.content.startswith('Press ') and message.channel.name.startswith('rules') and channel.guild== guild:
			await message.add_reaction('<a:ru:667688111995748352>')
client = MyClient()
client.run(open("id.txt", "r").read())