#!/usr/bin/python
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import codecs

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Bot"
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE bot_guilds(guild_id TEXT(20))")


sql_send_guild_id_bot = "INSERT INTO bot_guilds (guild_id) VALUES (%s)"

def guild_id_sql():
    mycursor.execute("SELECT * FROM bot_guilds")
    myresult = mycursor.fetchall()
    for raw in myresult:
        if raw[0] == "288021686329016321" :
            print("---- %s"%(raw[0]))

sql = "INSERT INTO bot_guilds (guild_id) VALUES (%s)"


TOKEN = 'NDc4MTIyMTcwOTYzMzI5MDUw.Xugoxg.fO0fSDroIp4HkM-wHd7IpqYTBwg'
client = commands.Bot(command_prefix="|")

def guild_id():
    guild_id = []
    for i in client.guilds:
        g_id = i.id
        guild_id.append(g_id)
        mycursor.execute(sql, (g_id,))
    mydb.commit()

    return guild_id


@client.event
async def on_ready():
    print("Bot Başladı")


@client.event
async def on_message(message):
    # Kendi mesajlarını komut olarak görmesini engelliyor
    if message.author == client.user:
        # Uyarı mesajını kendi mesajından bulup X saniye sonra siliyor
        if(message.content.find("Kelimelerini Dikkatli Seç") != -1):
            await asyncio.sleep(5)
            await message.delete()


    else:

        manage_msg = False
        print(message.content)
        this_msg = message.content.lower()
        mydbdjango = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="DjangoWebsite"
        )
        mycursordjango = mydbdjango.cursor()
        mycursordjango.execute("SELECT * FROM managebot_custom_command")
        myresultdjango = mycursordjango.fetchall()
        for r in myresultdjango:
            print(r[1])
            if r[1] == str(message.guild.id) :
                if(message.content.find(r[2]) != -1):
                    await message.channel.send(r[3])


    # Mesajların komut olarak işliyor
    await client.process_commands(message)




#https://discord.com/api/oauth2/authorize?client_id=478122170963329050&permissions=2134207679&guild_id=482532536807981056&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Flogin%2Fcallback%2F&scope=bot


@client.event
async def on_guild_join(guild):
    print("------{}".format(guild.id))

    zatenvar = False
    mycursor.execute("SELECT * FROM bot_guilds")
    myresult = mycursor.fetchall()
    for r in myresult:
        if r[0] == str(guild.id) :
            zatenvar = True

    if zatenvar == False :
        mycursor.execute(sql, (guild.id,))
        mydb.commit()
        print("data base kaydedildi", guild.id)

@client.event
async def on_guild_remove(guild):
    sql_delete_id = "DELETE FROM bot_guilds WHERE guild_id = %s"

    print("sunucudan cıkıldı ",guild.id)
    mycursor.execute(sql_delete_id, (guild.id,))
    mydb.commit()


# Chat Temizleme
@client.command(pass_context=False)
@commands.has_permissions(ban_members=True)
async def clearmax(ctx, amount: int):
    if(amount <= 200):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    else:
        await ctx.channel.send("lütfen 1 ile 30 arasında bir sayı giriniz")

# Chat Temizleme


@client.command(pass_context=False)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if(amount <= 30):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.channel.send("lütfen 1 ile 30 arasında bir sayı giriniz")


# Banlama
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=""):
    reason_c = "Risebot Kullanılarak %s Tarafından Banlandı Sebep : %s" % (
        ctx.message.author, reason)
    await member.ban(reason=reason_c)


# Kickleme
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=""):
    reason_c = "Risebot Kullanılarak %s Tarafından Kiklendi Sebep : %s" % (
        ctx.message.author, reason)
    await member.kick(reason=reason_c)
    await ctx.send("Yüce " + ctx.author + " Tarafından kiklendi")



# Mute
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=""):
    print("komut çalıştı")
    await member.edit(mute=True)
    reason_int = ''.join([n for n in reason if n.isdigit()])
    reason_int = int(reason_int)
    orjin_reason = reason
    if len(orjin_reason.split()) > 1:
        orjin_reason = orjin_reason.split(' ', 1)[1]
    else:
        orjin_reason = "Belirtilmemiş"

    reason = reason.lower()
    if reason_int > 0:
        if reason.find("dk") != -1:
            mute_timed = reason_int * 60
            embed = discord.Embed(colour=15158332)
            embed.set_author(name=f" {member} Kullanıcısı Mutelendi ! ", )
            embed.add_field(name=" Mutelenen Hesap  ", value=member.mention)
            embed.add_field(name=" Mute Süresi ",
                            value=f"{mute_timed//60} Dakika ")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(
                text=f"Muteleyen {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=" Sebep", value=f"{orjin_reason}")
            embed.add_field(name=" Bilgilendirme", value=f"Mutelenen Kullanıcı Eyer Sesli Odadaysa Mutesi Otamatik Olarak Acılacaktır. Mutenin Açılmasına 1 Dakika Kala Kullanıcı Sesli Odaya Geçmesi İçin Uyarılacaktır")
            await ctx.send(embed=embed)
            mute_timed = mute_timed - 60
            await asyncio.sleep(mute_timed)
            await ctx.send(f"<@!{member.id}> Mutenizin Açılmasına Son 1 Dakika Kaldı. Lütfen Mutenizin Otomatik Olarak Açılması İçin Bir Sesli Odaya Geçin Ve Bekleyin  ")
            await asyncio.sleep(60)
            await member.edit(mute=False)

        elif reason.find("sa") != -1:
            mute_timed = reason_int * 3600
            embed = discord.Embed(colour=15158332)
            embed.set_author(name=f" {member} Kullanıcısı Mutelendi ! ", )
            embed.add_field(name=" Mutelenen Hesap  ", value=member.mention)
            embed.add_field(name=" Mute Süresi ",
                            value=f"{mute_timed//3600} saat ")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(
                                text=f"Muteleyen {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=" Sebep", value=str(orjin_reason))
            embed.add_field(name=" Bilgilendirme", value=f"Mutelenen Kullanıcı Eyer Sesli Odadaysa Mutesi Otamatik Olarak Acılacaktır. Mutenin Açılmasına 1 Dakika Kala Kullanıcı Sesli Odaya Geçmesi İçin Uyarılacaktır")
            await ctx.send(embed=embed)
            mute_timed = mute_timed - 60
            await asyncio.sleep(mute_timed)
            await ctx.send(f"<@!{member.id}> Mutenizin Açılmasına 1 Dakika Kaldı. Lütfen Mutenizin Otomatik Olarak Açılması İçin Bir Sesli Odaya Geçin Ve Bekleyin  ")
            await asyncio.sleep(mute_timed)
            await member.edit(mute=False)


#Mute kaldırma
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, *, reason="Belirtilmedi"):
    await member.edit(mute=False)
    embed = discord.Embed(colour=15844367)
    embed.set_author(name=f" {member} Kullanıcısının Mutesi kaldırıldı ", )
    embed.add_field(name=" Mutesi Kaldırılan Hesap  ", value=member.mention)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text=f"Muteleyen {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.add_field(name=" Sebep", value=str(reason))
    await ctx.send(embed=embed)


#Kullanıcı bilgisi verir ve chate kaydeder
@client.command()
async def userinfo(ctx, member: discord.Member):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color,
                          timestamp=ctx.message.created_at)

    embed.set_author(name=f"Kullanıcı Bilgisi - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text=f"Sorgulama Yapan {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="İD:", value=member.id)
    embed.add_field(name="Sunucu İsmi: ", value=member.display_name)

    embed.add_field(name="Hesabın Oluşturulma Tarihi ",
                    value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Hesabın Sunucuya Girş Tarihi ",
                    value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Permleri ({len(roles)})", value=" ".join(
        [role.mention for role in roles]))
    embed.add_field(name="En Yüksek Permi: ", value=member.top_role.mention)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


#Komutu çalıştıran kişi bir odada ise o odaya bağlanır
@client.command()
@commands.has_permissions(ban_members=True)
async def join(ctx):

    channel = ctx.message.author.voice.channel
    print(channel)
    await channel.connect()


#Komut çalıştığında odadan ayrılır
@client.command()
@commands.has_permissions(ban_members=True)
async def leave(ctx):
    if not ctx.voice_client is None:
        await ctx.voice_client.disconnect()

    else:
        channel = ctx.message.author.voice.channel
        print(channel)
        await channel.connect()
        voice_client = ctx.guild.voice_client
        channel = voice_client.channel
        await voice_client.main_ws.voice_state(ctx.guild.id, channel.id, self_mute=True)
        await ctx.voice_client.disconnect()


client.run(TOKEN)
