import discord
from discord.ext import commands
import sqlite3

def get_prefix(bot,message):
	c.execute("SELECT * FROM prefixes WHERE id="""+str(message.guild.id))
	try:return commands.when_mentioned_or(c.fetchone()[1])(bot,message)
	except:return commands.when_mentioned_or('!')(bot,message)
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command("help")
@client.command(case_insenitive=True, aliases=["calc", "math"])
async def calculate (ctx, *, operation=None):
    try:
        operation = eval(operation)
    except ZeroDivisionError:
        await ctx.send("Error: division by zero")
        return
    except:
        await ctx.send("Error: expression could not be calculated")
        return
    await ctx.send(operation)

client.run(open("id.txt", "r").read())