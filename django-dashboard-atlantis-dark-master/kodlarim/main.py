from allauth.socialaccount.providers.discord.provider import DiscordProvider

from allauth.socialaccount.models import SocialAccount,SocialToken
import decimal
import requests

def  all_administrator_guilds(request):

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
            else:
                pass
            guilds_while_len += 1
        return guilds_administrator




    guilds_administrator = guild_content(guilds_data)

    return guilds_administrator
