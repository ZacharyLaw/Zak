import discord
import pandas as pd
import os
import sys
import re
import csv
#ID,IGN,SupportID,Fb
#270864978569854976,ZacharyLaw,6736638272077824,http://www.facebook.com/law.zac.50
profile=pd.read_csv('profile.csv', index_col=0,dtype=str)
profile['Facebook']='[Link]('+profile['Fb']+')'
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print('Running '+ os.path.basename(__file__))
	async def on_message(self, message):
		arg = message.content.split()
		if message.author.id == self.user.id or not (message.content.startswith('!') or message.content.startswith('+') or message.content.startswith('-')):pass		
		elif message.content.startswith('!profile'):
			if len(arg)==1:
				try:
					authorprofile=profile.loc[[message.author.id]]
					embed = discord.Embed(description=authorprofile[['IGN','SupportID','Facebook']].transpose().dropna().to_string(header=False).replace('  ','').replace('IGN','IGN: ').replace('SupportID','SupportID: ').replace('Facebook','Facebook: '),colour=discord.Colour.from_rgb(47,49,54))
					await message.channel.send(embed=embed)
				except:await message.channel.send('Profile not found')
			elif message.mentions:
				try:
					authorprofile=profile.loc[[message.mentions[0].id]]
					embed = discord.Embed(description=authorprofile[['IGN','SupportID','Facebook']].transpose().dropna().to_string(header=False).replace('  ','').replace('IGN','IGN: ').replace('SupportID','SupportID: ').replace('Facebook','Facebook: '),colour=discord.Colour.from_rgb(47,49,54))
					await message.channel.send(embed=embed)
				except:await message.channel.send('Profile not found')
			elif re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content):
				if message.author.id in profile.index:profile.loc[message.author.id,'Fb']=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content)[0]
				else:profile.loc[message.author.id]=[None,None,re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content)[0],None]
				os.remove('profile.csv')
				profile[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
			elif re.findall('\d{16}',message.content.replace('!profile ','')):
				if message.author.id in profile.index:profile.loc[message.author.id,'SupportID']=re.findall('\d{16}',message.content.replace('!profile ',''))[0]
				else:profile.loc[message.author.id]=[None,re.findall('\d{16}',message.content.replace('!profile ',''))[0],None,None]
				os.remove('profile.csv')
				profile[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
			elif re.findall('\w{4,16}',message.content.replace('!profile ','')):
				if message.author.id in profile.index:profile.loc[message.author.id,'IGN']=re.findall('\w{4,16}',message.content.replace('!profile ',''))[0]
				else:profile.loc[message.author.id]=[re.findall('\w{4,16}',message.content.replace('!profile ',''))[0],None,None,None]
				os.remove('profile.csv')
				profile[['IGN','SupportID','Fb']].to_csv('profile.csv')
				await message.add_reaction('👌')
client = MyClient()
client.run(open("id.txt", "r").read())