import nextcord
from nextcord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='.', intents=nextcord.Intents.all())

promotion_channels = {}

@bot.event
async def on_guild_join(guild):
    promotion_channels[guild.id] = None
    await guild.owner.send("Thanks for inviting me! Please use `.setchannel`")

    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        owner = guild.owner
        await owner.send(f"Hello, {owner.display_name}! Please use the `.setchannel` command again.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setchannel(ctx, channel: nextcord.TextChannel):
    promotion_channels[ctx.guild.id] = channel
    await ctx.send(f"Promotions will be sent in {channel.mention}.")

@bot.command()
async def promote(ctx, invite_link: str):
    if '@everyone' in invite_link or '@here' in invite_link:
        await ctx.guild.ban(ctx.author, reason="Don't use those mentions.")
        await ctx.send("You can't use those mentions in the invite link.")
        return
    
    for guild_id, promotion_channel in promotion_channels.items():
        if promotion_channel is None or guild_id == ctx.guild.id:
            continue

        try:
            guild = bot.get_guild(guild_id)

            # Create an embed for promotion
            embed = nextcord.Embed(
                title=f"Join our server: {guild.name}",
                description=f"Discord Invite Link: {invite_link}",
                color=0x00ff00  # Green color
            )
            embed.set_footer(text=f"Promoted by: {ctx.author.name}")

            await promotion_channel.send(embed=embed)
            await ctx.author.send(f"Server invite sent successfully to {guild.name}!")
        except Exception as e:
            await ctx.send(f"Failed to send the server invite to {guild.name}. Error: {str(e)}")

bot.run(token)






