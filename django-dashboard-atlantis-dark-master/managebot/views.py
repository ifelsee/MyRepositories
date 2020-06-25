


from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse , HttpResponseRedirect
from django import template
from kodlarim import main
from .forms import CustomCommandForm


from allauth.socialaccount.models import SocialAccount,SocialToken
import requests

import mysql.connector
# Create your views here.



#mycursor.execute("CREATE TABLE bot_guilds(guild_id TEXT(20))")

@login_required(login_url="/login/")
def index(request, guild_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="Bot"
    )
    mycursor = mydb.cursor()
    this_user_guild= main.all_administrator_guilds(request)
    for g in this_user_guild:
        if g[3] == guild_id:
            mycursor.execute("SELECT * FROM bot_guilds")
            myresult = mycursor.fetchall()
            for raw in myresult:
                print(raw[0])
                if g[3]== raw[0]:
                    print(request.POST)
                    form = CustomCommandForm()
                    if request.method == "POST":
                        post_form = CustomCommandForm(request.POST)
                        if post_form.is_valid():
                            post = post_form.save(commit=False)
                            post.guild_id = g[3]
                            post.save()


                    print("Yönetebilir --- ",g[0])
                    context = {
                    "guildName":g[0],
                    "guildİd":g[3],
                    "guildİcon":g[4],
                    "form":form,
                    }

                    return render(request,"manage.html",context)

            return HttpResponseRedirect("https://discord.com/api/oauth2/authorize?client_id=478122170963329050&permissions=0&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Flogin%2Fcallback%2F&scope=bot")

    return HttpResponse("Birşeyler Yanlış Gitti")
