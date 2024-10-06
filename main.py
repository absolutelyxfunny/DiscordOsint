import discum
from discord.ext import commands
import requests

token = ""
bot = discum.Client(token = f'{token}')
client = commands.Bot(command_prefix="*", self_bot = True)


headers = {
	"authorization": token
}


server_id = int(input("Enter ServerID >> "))
channel_id = int(input("Enter ChannelID >> "))

server = requests.get(f"https://discord.com/api/v9/guilds/{server_id}", headers=headers).json()
server_name = server["name"]


members_id = []
global_names = []
usernames = []
ids = []


def close_after_fetching(resp, guild_id):
	if bot.gateway.finishedMemberFetching(guild_id):
		lenmembersfetched = len(bot.gateway.session.guild(guild_id).members) 
		print(str(lenmembersfetched)+' members fetched') 
		bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
		bot.gateway.close()


def update_members(resp, guild_id):
	if resp.event.guild_member_list:
		
		members = bot.gateway.session.guild(guild_id).members
		for user, names in members.items():
			
			presence = names["presence"]
			user = presence["user"]
			

			id = user.get("id")
			if id in members_id:
				continue
			members_id.append(id)
			username = names.get("username")
			global_name = names.get("global_name")
			is_bot = names.get("bot")
			
			if is_bot == True:
				continue
			if id in members_id:
			    with open("profiles.txt", "a", encoding="utf-8") as file:
			    	file.write(f"ID: {id} | UserName: {username} |  GlobalName: {global_name} | ServerID: {server_id} | ServerName: {server_name}\n")
			
			
			


def get_members(guild_id, channel_id):
	bot.gateway.fetchMembers(guild_id, channel_id, keep="all") 
	bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
	bot.gateway.command({'function': update_members, 'params': {'guild_id': guild_id}})
	bot.gateway.run()
	bot.gateway.resetSession() 

members = get_members(f"{server_id}", f"{channel_id}") 


