# -*- coding: utf-8 -*- 
import os
import discord
from discord.ext import commands
import asyncio
from mcstatus import MinecraftServer
from datetime import datetime

# import logging #In case you would like to save data

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

if __name__ == "__main__":

    token = 'NjYwMjAyMTc1NTYxMDcyNjgw.Xh4sJA.e_VA9J-SH2g1xndUrALY6TP0txc'
    server_ip = 'play.LukyCraft.cz'

    client = discord.Client()
    client = commands.Bot(command_prefix="!")
    client.remove_command('help')
    

    @client.event
    async def on_ready():
        print("LukyCraft BOT has connected to Discord!")
        print("Connecting to {}".format(server_ip))
        
    @client.event
    async def update():
        while True:
            await client.wait_until_ready()
            try:
                server = MinecraftServer.lookup(server_ip)
                status = server.status()
                name = "Online"
    
                await client.change_presence(status = discord.Status.online,
                                             activity = discord.Game(f'{status.players.online}/20'))

                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("Server Name: {}".format(name))
                print("Server Ping: {}".format(status.latency))
                print("Players Online: {}\n".format(status.players.online))

            except:
                activity = discord.Game(name="Server Offline")
                await client.change_presence(status = discord.Status.dnd,
                                             activity = activity)
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("Cannot connect to server\n")

            await asyncio.sleep(5)
        
    ##Neplatný argument##
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**Chyba:** Nenapsal jsi platný argument!')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('**Chyba:** Tento příkaz neexistuje!')

    @client.command() 
    @commands.has_permissions(kick_members=True)
    async def bc(ctx, *, args, amount=1):
        await ctx.channel.purge(limit=amount)
        await ctx.send(args)

    @client.command(aliases=['cc','clearchat'])
    @commands.has_permissions(kick_members=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @client.command()
    @commands.has_permissions(kick_members=True)
    async def ban(ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Uživatel {member} byl zabanován kvůli {reason}!')
        print(f"Banned {member}. Reason : {reason}") 

    @client.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Uživatel {member} byl vykopnut kvůli {reason}!')
        print(f"Kicked {member}. Reason : {reason}")

    @client.command()
    @commands.has_permissions(kick_members=True)
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Uživatel {user.mention} byl odbanován!')
                print(f"Unbanned {user.name}#{user.discriminator}")
                return

    @client.command()
    @commands.has_permissions(administrator=True)
    async def restart(ctx):
        await ctx.send("**Restarting...!**")
        await client.logout()

    @client.command()
    async def help(ctx):
        await ctx.send(':pushpin: **Příkazy:**')
        await ctx.send("""
    ```
    !help - zobrazí tento seznam
    !ping - napíše ping bota
    !ip - zobrazí server IP
    !vip - návod jak si koupit vip
    !autor - zobrazí tvůrce bota
    ```
    """)

    @client.command()
    @commands.has_permissions(kick_members=True)
    async def adminhelp(ctx):
        await ctx.send(':pushpin: **Admin Příkazy:**')
        await ctx.send("""
    ```
    Admin:
    !adminhelp - zobrazí tento seznam
    !clear <počet zprav> - vymaže <počet zprav>
    !restart - restartuje bota (pouze pro administrátora)
    !bc <zpráva> - sdělí zprávu
    !ban <uživatel> - zabanuje uživatele
    !unban <uživatel> - odbanuje uživatele
    !kick <uživatel> - vykopne uživatele ze serveru
    Default:
    !help - zobrazí seznam default příkazů
    !ping - napíše ping bota
    !ip - zobrazí server IP
    !vip - návod jak si koupit vip
    !autor - zobrazí tvůrce bota
    ```
    """)

    ##Neplatný príkaz##
    @unban.error
    async def unban_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**Použití:** !unban <uživatel>')

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**Použití:** !ban <uživatel> <důvod>')

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**Použití:** !kick <uživatel> <důvod>')

    @client.command()
    async def ping(ctx):
        await ctx.send(f'**Ping od Bota k Discord serveru:** {round(client.latency * 1000)}ms.')
        await ctx.send('Pokud je ping moc velký napiš prosím do kanálu #chyby :)')

    @client.command()
    async def ip(ctx):
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

        embed.set_author(name="IP Minecraft serveru:", icon_url=ctx.author.avatar_url)

        embed.add_field(name="LukyCraft IP:", value="play.LukyCraft.cz")

        await ctx.send(embed=embed)

    @client.command()
    async def autor(ctx):
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

        embed.set_author(name="Bota vytvořili:", icon_url=ctx.author.avatar_url)

        embed.add_field(name="Tomasko63 (Thomas_29)", value="Vytvořil 90% bota.", inline=False)
        embed.add_field(name="JustF0X (JustF0XStudios)", value="Dělal to, co Tomasko63 nevěděl.", inline=False)

        await ctx.send(embed=embed)

    @client.command()
    async def vip(ctx):
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

        embed.set_author(name="💎 VIP 💎", icon_url=ctx.author.avatar_url)

        embed.add_field(name="CZ na 30 dnů", value="Cena: 50kč, Číslo: 90733, Text SMS: csmc 50 s210881 <Tvůj nick>", inline=False)
        embed.add_field(name="CZ na vždy", value="Cena: 99Kč, Číslo: 90733, Text SMS: csmc 99 s210881 <Tvůj nick>", inline=False)
        embed.add_field(name="SK na 30 dnů", value="Cena: 2€, Číslo: 8877, Text SMS: csmc 2 s210881 <Tvůj nick>", inline=False)
        embed.add_field(name="SK na vždy", value="Cena: 4€, Číslo: 8877, Text SMS: csmc 4 s210881 <Tvůj nick>", inline=False)

        await ctx.send(embed=embed)

    @client.command()
    async def info(ctx):
        # Info
        await ctx.send(f"Tento status byl nahrazen, mrkni vpravo nahoru :wink: ")
        

    client.loop.create_task(update())
    client.run(token)
