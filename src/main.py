import json
from discord import Client, ActivityType

class KrodenBot(Client):

    @property
    def token(self):
        return self.config['token']

    def __init__(self):
        self.config = {}
        self.load_config()
        super().__init__()

    def load_config(self):
        config_file = open('config.json', 'r', encoding='utf-8')
        config_text = config_file.read()
        config_file.close()
        self.config = json.loads(config_text, encoding='utf-8')

    async def on_guild_available(self, guild):
        await self.update_voice_channels(guild)
        await self.check_member_roles(guild)

    async def on_member_update(self, before, after):
        await self.update_voice_channels(after.guild)
        await self.check_member_roles(after.guild)

    async def on_voice_state_update(self, member, before, after):
        await self.update_voice_channels(member.guild)

    async def on_guild_role_create(self, role):
        for guild in self.guilds:
            await self.check_member_roles(guild)

    async def on_guild_role_update(self, role):
        for guild in self.guilds:
            await self.check_member_roles(guild)

    def get_member_current_game(self, member):
        for activity in member.activities:
            if hasattr(activity, 'name') and \
               hasattr(activity, 'type') and \
               activity.type == ActivityType.playing:
                return self.get_role_by_game_name(activity.name)
            else:
                return None

    def get_role_by_game_name(self, game_name):
        for game_role in self.config['gameRoleMap']:
            if game_role['gameName'] == game_name:
                return game_role['roleName']
        return game_name

    def get_default_voice_channel_name(self, voice_channel):
        if 'voiceChannels' in self.config and \
           len(self.config['voiceChannels']) > voice_channel.position and \
           'name' in self.config['voiceChannels'][voice_channel.position]:
            return self.config['voiceChannels'][voice_channel.position]['name']
        else:
            return 'Lobby {}'.format(voice_channel.position + 1)

    async def check_member_roles(self, guild):
        for member in guild.members:
            game_role_name = self.get_role_by_game_name(self.get_member_current_game(member))
            if game_role_name:
                for member_role in member.roles:
                    if member_role.name == game_role_name:
                        break # user already has the role for the game they're playing

                    for guild_role in guild.roles:
                        if guild_role.name == game_role_name:
                            await member.add_roles(guild_role)

    # Update the name of the voice channel to whatever the most common game everybody in the channel is playing
    async def update_voice_channels(self, guild):
        for voice_channel in guild.voice_channels:

            # count the number of channel members that are playing each game
            channel_game_map = {}
            for voice_member in voice_channel.members:
                game_name = self.get_member_current_game(voice_member)
                if game_name in channel_game_map:
                    channel_game_map[game_name] += 1
                else:
                    channel_game_map[game_name] = 1

            # select the most commonly played game within the channel
            most_played_game = None
            most_players = 0
            for key in channel_game_map:
                if channel_game_map[key] > most_players:
                    most_played_game = key
                    most_players = channel_game_map[key]

            if most_played_game:
                new_channel_name = self.get_role_by_game_name(most_played_game)
            else:
                new_channel_name = self.get_default_voice_channel_name(voice_channel)

            # update the channel name if needed
            if new_channel_name != voice_channel.name:
                await voice_channel.edit(name=new_channel_name)


kroden_bot = KrodenBot()
kroden_bot.run(kroden_bot.token)
