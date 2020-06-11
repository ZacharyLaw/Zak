import discord
import os
client = discord.Client()
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
	async def on_message(self, message):
		if message.channel.id==567848114170494976 and message.author.id != self.user.id and message.author.bot:await message.delete()
		elif message.channel.id==567848114170494976 and message.author.id != self.user.id:
			embed = discord.Embed(description=message.content,colour=discord.Colour.from_rgb(47,49,54))
			embed.set_author(name=message.author,icon_url=message.author.avatar_url)
			embed.set_footer(text='Author only: 🗑️ To delete',icon_url='https://cdn.discordapp.com/attachments/674632751390916609/700745020994617428/invis.png')
			if message.attachments:embed.image(message.attachments[0].url)
			sugg=await message.channel.send(embed=embed)
			await sugg.add_reaction('<:upvote:592757143892000769>')
			await sugg.add_reaction('<:downvote:592757119069978644>')
			await sugg.add_reaction('🗑️')
			await message.delete()
			def check(reaction,user):return reaction.emoji=='🗑️'
			try:
				while True:
					reaction,user = await client.wait_for('reaction_add',timeout=30.0,check=check)
					if user == message.author:await sugg.delete()
					else:await sugg.remove_reaction(reaction,user) 
			except:
				embed.set_footer(text='')
				await sugg.edit(embed=embed)
				await sugg.remove_reaction('🗑️',self.user) 
client = MyClient()
client.run(open("id.txt", "r").read())