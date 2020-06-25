# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template


# Create your views here.
from allauth.socialaccount.providers.discord.provider import DiscordProvider

from allauth.socialaccount.models import SocialAccount,SocialToken
import decimal
import requests




@login_required(login_url="/login/")
def index(request):

    if request.user.is_authenticated == True  : # Kullanıcının Giriş Yapıp Yapmadığını Sorguluyor
        # Kullanıcı SuperUser ise devam eder
        if  request.user.is_superuser is False:
            AccessToken = SocialAccount.objects.filter(user=request.user, provider='discord')[0].extra_data["AccessToken"]

            print(AccessToken)

            guilds_url = 'https://discord.com/api/users/@me/guilds'
            headers = {
                'Authorization': 'Bearer {0}'.format(AccessToken),
                'Content-Type': 'application/json',
            }
            guilds_data = requests.get(guilds_url, headers=headers).json()
            guilds_data_len = len(guilds_data)

            def guild_content(guilds_data):
                guilds_len = len(guilds_data)
                guilds_while_len = 0
                guilds_administrator = []
                while guilds_while_len< guilds_len :
                    guild_name = str(guilds_data[guilds_while_len]["name"])
                    guild_id = str(guilds_data[guilds_while_len]["id"])
                    guild_owner = str(guilds_data[guilds_while_len]["owner"])
                    guild_icon = str(guilds_data[guilds_while_len]["icon"])
                    guild_permissions = str(guilds_data[guilds_while_len]["permissions"])
                    """print(guild_name)
                        print(guild_id)
                        print(guild_owner)
                        print(guild_permissions)
                        print(guild_icon)
                        print("\n")
                    """
                    if guild_permissions == "2147483647":
                        guild_profile = guild_name,guild_owner,guild_permissions,guild_id,guild_icon

                        guilds_administrator.append(guild_profile)
                    else:pass
                    guilds_while_len += 1

                return guilds_administrator


            guilds_administrator = guild_content(guilds_data)

            for guild in guilds_administrator:
                guild_name = guild[0]
                guild_owner = guild[1]
                guild_permissions = guild[2]
                guild_id = guild[3]
                guild_icon_url = guild[4]
                print("------------ " + guild_name,guild_owner,guild_permissions,guild_id,guild_icon_url ,"\n")

                # AnonymousUser hatası alamak için guild sunucusu olup olmadığını içeride sorguluyorum

            context= {"durum":guilds_administrator}

        #SuperUser sogu
        else:
            context= {"durum":"SuperUser Sayfası"}

    else:
        context= {"durum":"Ziyaretci Sayfası "}


    return render(request,"index.html",context)





@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))
