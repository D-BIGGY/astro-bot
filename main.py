import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import os
from gameone import Person
import requests
import json


character = Person("", 0, 0, 0, 0, 0, "", "")
prefisso = "BIGGY "
#informazioni sul bot, qui si può cambiare il prefisso
client = commands.Bot(command_prefix=prefisso, intents=discord.Intents.all(),help_command=None)


#comando del saluto del bot
@client.command()
async def hello(ctx):
  await ctx.send("hello!")


#quello che viene scritto quando il bot è avviato e può runnare i comandi


@client.event
async def on_ready():
  prfx = (Back.BLACK + Fore.GREEN +
          time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET +
          Fore.WHITE + Style.BRIGHT)
  print(prfx + "Logged in as " + Fore.YELLOW + client.user.name)
  print(prfx + "Bot ID " + Fore.YELLOW + str(client.user.id))
  print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
  print(prfx + " Python Version " + Fore.YELLOW +
        str(platform.python_version()))


#


#comando shutdown
@client.command(aliases=[
  'smettila',
  'muori',
  'stop',
])  #aliases sono parole differenti ma che fanno comunque cominciare il comando
async def shutdown(ctx):
  await ctx.send("Adesso mi spengo")  #frase scritta allo spegnimento
  await client.close()


#


#comando per le informazini utente
@client.command(aliases=['uinfo', 'whois'])
async def userinfo(ctx, member: discord.Member = None):
  #chiedo come parametri il channel(ctx) e l'utente selezionato(=None significa che non è obbligatorio)
  #nel caso non venga inserito il nome di nessun utente allora le informazionin saranno riguardanti l'autore del messaggio
  if member == None:
    member = ctx.message.author
  roles = [role for role in member.roles]  #lista dei ruoli
  embed = discord.Embed(
    title="User info",
    description=f"Stalkerando con successo {member.mention}",
    color=member.accent_colour,
    timestamp=ctx.message.created_at)
  #mero tentativo di colorare la linea dell'embed con il colore principale dell'profilo dell'utente
  #l'embed è  quella specie di riquadro in cui sono presentate le informazioni riguardanti l'utente
  embed.set_thumbnail(url=member.avatar)
  #immagine profilo dell'utente
  embed.add_field(name="ID", value=member.id)
  #id dell'utente (serie di numeri identificativi)
  embed.add_field(name="Name", value=f"{member.name}#{member.discriminator}")
  #nome dell'utente [FF#2789]
  embed.add_field(name="Nickname", value=member.display_name)
  #nome all'interno del server dell'utente
  embed.add_field(name="Status", value=member.status)
  #stato dell'utente (online, offline ...)
  embed.add_field(
    name="Created At",
    value=member.created_at.strftime("%a, %B %#d, %Y, %I:&M %p "))
  #data di creazione dell'utente
  embed.add_field(name="Joined At",
                  value=member.joined_at.strftime("%a, %B %#d, %Y, %I:&M %p "))
  #data in cui l'utente è entrato a fare parte del server
  embed.add_field(name=f"Roles ({len(roles)})",
                  value="\n".join([role.mention for role in roles]))
  #lista di tutti i ruoli
  embed.add_field(name="Top Role", value=member.top_role.mention)
  #viene scritto il ruolo più alto della gerarchia che ha l'utente
  embed.add_field(name="Messages", value="0")
  #numero di messaggi scritti
  embed.add_field(name="Bot?", value=member.bot)
  #viene scritto se è un bot o meno
  await ctx.send(embed=embed)
  #invio l'embed


#


#comando per le informazioni del server
@client.command(aliases=['sinfo', 'server'])
async def serverinfo(ctx):
  embed = discord.Embed(
    title="Server info",
    description=f"Informazioni del server, {ctx.guild.name}",
    color=discord.Color.random(),
    timestamp=ctx.message.created_at)
  #creo l'embed
  embed.set_thumbnail(url=ctx.guild.icon)
  #visualizzo l'immagine del server
  embed.add_field(name="Members", value=ctx.guild.member_count)
  #scrivo quanti sono i membri presenti all'interno del server
  embed.add_field(
    name="Channels",
    value=
    f"{len(ctx.guild.text_channels)} text | {len(ctx.guild.voice_channels)} voice"
  )
  #scrivo quanti canali testuali e quanti canali vocali sono presenti nel server
  embed.add_field(name="Owner", value=ctx.guild.owner.mention)
  #viene scritto chi è il proprietario del server
  embed.add_field(name="Description", value=ctx.guild.description)
  #viene scritta la descrizione dle server
  embed.add_field(
    name="Created At",
    value=ctx.guild.created_at.strftime("%a, %B %#d, %Y, %I:&M %p "))
  #viene visualizzata la data in cuil il server è stato creato
  await ctx.send(embed=embed)
  #invio l'embed


#


@client.command(pass_context=True, aliases=['entra', 'join'])
async def Entra(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("Sono entrato nel canale vocale")

  else:
    await ctx.send(
      f"Non sei in un canale vocale {ctx.message.author.voice.channel} mostro")
  #


#


@client.command(pass_context=True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Adesso me ne vado")
  else:
    await ctx.send("Non sono in canale vocale")
  #


#


@client.command(aliases=['profile'])
async def GameProfile(ctx):
  embed = discord.Embed(
    title="Server info",
    description=f"Informazioni del personaggio, {ctx.guild.name}",
    color=discord.Color.random(),
    timestamp=ctx.message.created_at)
  embed.set_thumbnail(url=character.getPfp())
  #immagine profilo del personaggio
  embed.add_field(name="Name", value=character.getName())
  #nome del giocatore
  embed.add_field(name="Description", value=character.getDescription())
  #descrizione del personaggio
  embed.add_field(name="level", value=character.getLevel())
  #livello giocatore
  embed.add_field(name="Exp", value=character.getExp())
  #exp che ha il personaggio
  embed.add_field(name="Monete", value=character.getSoldi())
  #soldi personaggio
  embed.add_field(name="BiggyCoins", value=character.getBiggyCoins())
  #BiggyCoins del personaggio
  embed.add_field(name="Numero Amici", value=character.getAmici)


#


@client.command(aliases=["CP", "cp"])
async def ChangePrefix(ctx, arg):
  if arg == "":
    await ctx.send("non è stato inserito alcun prefisso")
  else:
    prefisso = arg
    await ctx.send("il prefisso del bot e' stato cambiato in: " + arg)


#


@client.command(aliases=["cn", "changeName"])
async def ChangeName(ctx, arg):
  if arg == "":
    await ctx.send("non è stato inserito alcun nome")
  else:
    character.setNome(arg)
    await ctx.send("il nome del tuo personaggio  è stato cambiato in: " + arg)


#


@client.command(aliases=["cd", "changeDescription"])
async def ChangeDescription(ctx, arg):
  if arg == "":
    character.setDesription(arg)
    await ctx.send("il messaggio è vuoto, la descrizione verrà cancellata")
  else:
    character.setDescription(arg)
    await ctx.send("la descrizione è stata cambiata")


#

@client.command(pass_context = True , aliases=["herp"])
async def help(ctx, arg=None):
  if arg == "character":
    embed = discord.Embed(
      title="character commands",
      description = "list of all the character commands",
      color = discord.Color.random(),
      timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=character.getPfp())
    embed.add_field(name="game profile", value=f"to gain informations about your character write {prefisso} GameProfile/profile")
    #character informations
    embed.add_field(name="Character name:", value=f"write {prefisso} ChangeName/changeName/cn [name] for changing your character name in the one you writed")
    #change character name
    embed.add_field(name="Character description", value=f"write {prefisso} ChangeDescription/changeDescription/cd [new description] for changing the description in the new one")
    #change character description
    await ctx.send(embed=embed)
  else:  
    embed = discord.Embed(
      title="commands info",
      description="Informazioni dei comandi",
      color=discord.Color.random(),
      timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=character.getPfp())
    #immagine profilo del personaggio
    embed.add_field(name="Joining a voice channel:", value= f"{prefisso} Entra/entra/join")
    #Comando BIGGY join
    embed.add_field(name = "Leaving a voice channel:", value=f"{prefisso} leave")
    #Comando BIGGY leave
    embed.add_field(name= "User informations:", value=f"{prefisso} userinfo/uinfo/whois will give informations about the user")
    #Comando BIGGY uinfo
    embed.add_field(name="Server info:", value=f"{prefisso} sinfo/server/serverinfo")
    #Comando sinfo
    embed.add_field(name="Character informations:", value=f"to obtain more informations about this topic write {prefisso} help character")
    #comando per ottenere informazioni sul personaggio
    await ctx.send(embed=embed)
    
    
      
client.run(os.getenv('TOKEN'), reconnect=True)
