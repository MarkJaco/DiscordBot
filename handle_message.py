"""
class for handling discord messages
"""
import poll
from threading import Timer


class MessageHandler:
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.current_poll = None

    async def reset_poll(self):
        await self.current_poll.end_poll()

    async def votekick(self, clean_message, message):
        """
        votekick certain user
        Args:
            clean_message: message command without 359!
            message: actual message object
        Returns:
            None
        """
        kick_user = clean_message[len("votekick")+1:]
        # go through all members on server
        kick_member = None
        for member in message.author.guild.members:
            nickname = member.nick.lower() if member.nick else None
            if nickname == kick_user or member.name.lower() == kick_user:
                kick_member = member
                break
        # no member with given name
        if not kick_member:
            await message.channel.send(f"Keinen solchen Benutzer gefunden.")
            return
        # member found, start vote
        votekick_poll = poll.Poll(kick_member, message.channel, 20)
        # kick user from voice channel if successful
        votekick_poll.successful = lambda m: m.edit.voice_channel(None)
        # start poll
        await votekick_poll.start_poll(f"Starte votekick für {kick_user}")

    async def handle_message(self, message):
        """
        handle message in different branches
        Args:
            message: the message received on discord
        Returns:
            None
        """
        # filter bot messages and not directed messages
        if message.author.id == self.bot_id or not message.clean_content.startswith("359! "):
            return

        # clean up message as string
        clean_message = message.clean_content[5:].lower()
        # get rid of author tag
        author_name = str(message.author)[:-5]

        # real commands
        if clean_message == "lösch dich":
            await message.channel.send(f"lösch dich selber @{author_name}")

        elif clean_message.startswith("votekick"):
            await self.votekick(clean_message, message)

