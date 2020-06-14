import discord
import asyncio
import os
client = discord.Client()
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
	async def on_message(self, message):
		if message.channel.id==487232049938300939 and (message.content.startswith('!open') or message.content.startswith('!blue')):
			await message.delete()
			await message.channel.edit(name='build🔵help')
		if message.channel.id==683680285434445914 and (message.content.startswith('!open') or message.content.startswith('!blue')):
			await message.delete()
			await message.channel.edit(name='build🔵help2')
		elif message.channel.id==487232049938300939 and not (message.content.startswith('!open') or message.content.startswith('!blue')):
			try:
				if message.channel.name=='build🔵help':await message.channel.edit(name='build🔴help')
				def check(m):return m.channel.id == 487232049938300939
				await client.wait_for('message',timeout=1200,check=check)
			except:
				await message.channel.edit(name='build🔵help')
		elif message.channel.id==683680285434445914 and not (message.content.startswith('!open') or message.content.startswith('!blue')):
			try:
				if message.channel.name=='build🔵help2':await message.channel.edit(name='build🔴help2')
				def check(m):return m.channel.id == 683680285434445914
				await client.wait_for('message',timeout=1200,check=check)
			except:
				await message.channel.edit(name='build🔵help2')
		
client = MyClient()
client.run(open("id.txt", "r").read())