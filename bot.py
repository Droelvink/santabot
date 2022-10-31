from tkinter import X
import discord
import random
import itertools

intents = discord.Intents.all()
client = discord.Client(intents = intents)

takenlist = []

dennis_id = 0 #OWNER ID HERE
exceptions = []

dm_message = """
Gegroet {0},
Kerst zit er weer aan te komen en er zijn weer groepjes gemaakt voor de gedichten en cadeau's!

+ Je zit dit jaar samen in de groep met:
{1}

+ En jullie mogen dit jaar cadeau's kopen en gedichten schrijven voor:
{2}

Dit jaar is het bedrag per persoon 15 euro
Alvast veel plezier tijdens kerst!

Groeten,
Santa Chad
"""

class MemberData:
    members:list[discord.Member] = []
    gifting:list[discord.Member] = []

    def __init__(self, members) -> None:
        self.members = members

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message:discord.Message):
    if message.author == client.user or not message.content.startswith('!'):
        return
    elif message.author.id != dennis_id:
        with open('nonono.gif', 'rb') as f:
            picture = discord.File(f)
            await message.reply(file=picture)
        return
    
    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')
    elif message.content.startswith('!sendhelp'):
        teams = None
        while(teams is None or len(teams) == 0 or contains_faults(teams)):
            teams = create_teams(message)

        for team in teams.keys():
            for member in teams[team].members:
                str = dm_message.format(member.display_name, format_members(list(filter(lambda x: x.id != member.id, teams[team].members))), format_members(teams[team].gifting))
                await message.author.send(f'```diff\n{str}```')

    elif message.content.startswith('!spam'):
        members = list_members(message)
        for member in members:
            str = dm_message.format('Neighbor', '* Persoon 1\n* Persoon 2\n* Persoon 3', '* Persoon 1\n* Persoon 2\n* Persoon 3')
            await member.send(f'```diff\n{str}```')

def create_teams(message:discord.Message):
    takenlist = []
    members = list_members(message)
    random.shuffle(members)

    teams:dict[int, MemberData] = dict()
    teamvan4 = 2
    teamcount = 0

    while(len(members) > 0):
        teamsize = 4 if teamvan4 > 0 else 3
        teams[teamcount] = MemberData(members[:teamsize])
        members = members[teamsize:]
        teamvan4 -= 1
        teamcount += 1

    for team in teams.keys():
        other_groups = list(filter(lambda data: data[0] != team , teams.items()))

        all_found_members = list(filter(lambda member: member not in takenlist, flatten(map(lambda data: data[1].members, other_groups))))
        random.shuffle(all_found_members)
        found_members = all_found_members[:len(teams[team].members)]
        teams[team].gifting = found_members

        for fm in found_members:
            takenlist.append(fm)

        if len(all_found_members) == 0:
            return []
    
    return teams

def format_members(members):
    str = ''
    for member in members:
        str += f'* {name_format(member)}\n'
    return str

def contains_faults(teams:dict[int, MemberData]):
    for team in teams:
        for exception in exceptions:
            if exception[0] in map(lambda x: x.id, teams[team].members) and exception[1] in map(lambda x: x.id, teams[team].members):
                return True
        if len(teams[team].members) is not len(teams[team].gifting):
            return True
    return False


def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))

def list_members(message:discord.Message):
    return list(filter(lambda member: member.id != client.user.id and len(list(filter(lambda rolename: rolename == 'team-deelnemer', map(lambda role: role.name, member.roles)))) > 0, message.guild.members))

def name_format(member:discord.Member):
    return f'{member.display_name} ({member.name})'

client.run('DISCORD_TOKEN_HERE')