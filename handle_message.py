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
        self.current_poll = None

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
        votekick_poll = poll.Poll(kick_member, message.channel)
        self.current_poll = votekick_poll
        # kick user from voice channel if successful
        votekick_poll.successful = lambda m: m.edit.voice_channel(None)
        # start poll
        await votekick_poll.start_poll(f"Starte votekick für {kick_user}")

    async def handle_votes(self, clean_message, message):
        """
        handles votes for polls
        Args:
            clean_message: message as cleaned up string
            message: message object
        Returns:
            None
        """
        # poll doesn't exist
        if not self.current_poll:
            await message.author.channel.send("Es läuft momentan keine Abstimmung.")
            return
        # poll does exist
        if clean_message.startswith("f1"):
            self.current_poll.votes_in_favor += 1
        elif clean_message.startswith("f2"):
            self.current_poll.votes_against += 1
        # add member who voted to list
        self.current_poll.members_voted.append(message.author)

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
            # don't start two polls at the same time
            if not self.current_poll:
                await self.votekick(clean_message, message)
            else:
                await message.author.channel.send("Eine Abstimmung läuft bereits")

        elif clean_message.startswith("f1") or clean_message.startswith("f2"):
            await self.handle_votes(clean_message, message)
