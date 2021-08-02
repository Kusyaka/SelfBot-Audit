import os

import discord
from discord.ext import commands
import json
import datetime


def getFile(guild, author=None, dm=None):
    path = f"logs/guild/{guild.id}.json" if guild is not None else f"logs/dm/{author.id}.json"
    if os.path.exists(path):
        return json.load(open(path, "r")), path

    if guild is not None:
        return {"guid_name": guild.name,
                "guild_id": guild.id,
                "guild_icon": str(guild.icon_url),
                "is_guild": True,
                "events": []
                }, path

    return {"DM_name": str(dm),
            "DM_id": dm.id,
            "DM_user_id": dm.recipient.id,
            "DM_icon": str(dm.recipient.avatar_url),
            "is_guild": False,
            "events": []
            }, path


def saveFile(file, path):
    with open(path, "w") as f:
        json.dump(file, f, indent=2)


class EventHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        file, path = getFile(message.guild, message.author, message.channel)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Message Delete",
            "author": str(message.author),
            "author_id": message.author.id,
            "author_icon": str(message.author.avatar_url),
            "content": message.content,
            "attachments": [o.url for o in message.attachments],
            "jump_url": message.jump_url
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for msg in messages:
            await self.on_message_delete(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        file, path = getFile(before.guild, before.author)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Message Edit",
            "author": str(before.author),
            "author_id": before.author.id,
            "author_icon": str(before.author.avatar_url),
            "before_content": before.content,
            "before_attachments": [o.url for o in before.attachments],
            "after_content": after.content,
            "after_attachments": [o.url for o in after.attachments],
            "jump_url": before.jump_url
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        file, path = getFile(channel.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Channel Create",
            "channel_id": channel.id,
            "channel_type": channel.type.name,
            "channel_name": channel.name,
            "category_name": channel.category.name,
            "category_id": channel.category.id,
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        file, path = getFile(channel.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Channel Delete",
            "channel_id": channel.id,
            "channel_type": channel.type.name,
            "channel_name": channel.name,
            "category_name": channel.category.name,
            "category_id": channel.category.id,
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        file, path = getFile(before.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Channel Update",
            "channel_id": before.id,
            "channel_type": before.type.name,
            "before_channel_name": before.name,
            "after_channel_name": after.name,
            "before_nsfw": before.nsfw,
            "after_nsfw": after.nsfw,
            "before_topic": before.topic,
            "after_topic": before.topic,
            "before_slowmode_delay": before.slowmode_delay,
            "after_slowmode_delay": after.slowmode_delay,
            "category_name": before.category.name,
            "category_id": before.category.id,
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        file, path = getFile(member.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Member Join",
            "avatar_url": member.avatar_url,
            "name": str(member)
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        file, path = getFile(member.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Member Join",
            "avatar_url": member.avatar_url,
            "name": str(member)
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        file, path = getFile(before.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Member Join",
            "before_avatar_url": str(before.avatar_url),
            "after_avatar_url": str(after.avatar_url),
            "before_name": str(before),
            "after_name": str(after),
            "before_roles": [str(r) for r in before.roles],
            "after_roles": [str(r) for r in after.roles]
        })
        saveFile(file, path)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        pass
        file, path = getFile(before.guild)
        file["events"].append({
            "timestamp": int(datetime.datetime.utcnow().timestamp()),
            "type": "Member Join",
            "before_avatar_url": before.avatar_url,
            "after_avatar_url": after.avatar_url,
            "before_name": str(before),
            "after_name": str(after),
            "before_roles": [str(r) for r in before.roles],
            "after_roles": [str(r) for r in after.roles]
        })
        saveFile(file, path)



bot = commands.Bot(command_prefix="_", self_bot=True)
bot.add_cog(EventHandler(bot))
with open("settings.json", "r") as f:
    bot.run(json.load(f)["DiscordUserToken"], bot=False)
