import discord
from discord.ext import commands
import sqlite3
import random as r
conn = sqlite3.connect("batteries.db")
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY KEY, username TEXT, batteries INTEGER DEFAULT 0 ) """)
conn.commit()
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    print(f'Bot {bot.user} launched!')

    
@bot.command()
async def send(ctx, amount: int):
    user_id = ctx.author.id
    username = ctx.author.name
    cursor.execute("SELECT batteries FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        new_total = result[0] + amount
        cursor.execute("UPDATE users SET batteries = ? WHERE user_id = ?", (new_total, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, username, batteries) VALUES (?, ?, ?)", (user_id, username, количество))
    conn.commit()
    await ctx.send(f'✅ {ctx.author.mention}, You have successfully send {amount} batteries! A total of {new_total} have been send.')

    
advices = [
    "Why is it important to recycle batteries? One discarded battery can pollute 20 square meters of soil with heavy metals. By recycling it, you help protect nature!",
    "Never throw batteries in the regular trash! They contain toxic substances: lead, mercury, cadmium. These elements can get into water and soil.",
    "How to properly prepare batteries for recycling? Collect them in a sealed container (for example, a plastic bottle) and store them until you visit a collection point. Do not open or damage them!"
    "What happens to batteries after recycling? Metals, graphite, and other valuable materials are extracted from them. These materials are then reused — this saves the planet's resources."
    ]
@bot.command()
async def advice(ctx):
    adv = advices[r.randint(0,len(advices)-1)]
    await send(f'Advice: {adv}')



class MyView(discord.ui.View):
    @discord.ui.button(label="Advice",style=discord.ButtonStyle.primary)
    async def bc_advice(self, interaction: discord.Interaction, button: discord.ui.Button):
        adv = advices[r.randint(0,len(advices)-1)]
        await interaction.response.send_message(f'Advice: {adv}')

    @discord.ui.button(label="Send batteries",style=discord.ButtonStyle.primary)
    async def bc_send(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('You have successfully send 10 batteries!')
@bot.command()
async def buttons(ctx):
    await ctx.send('What do you want to do?',view = MyView())
bot.run("TOKEN")
