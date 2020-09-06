"""
this module handles Polls

for example kicking someone from a voice channel
"""
import time
import discord.errors


class Poll:
    """
    new Poll, needs member to make poll about
    member is a member object from discord.py
    channel object which channel to write into
    time_limit how long poll should last in seconds
    """

    def __init__(self, member, channel, time_limit):
        self.member = member
        self.channel = channel
        self.time_limit = time_limit
        self.successful = None
        self.members_voted = []
        self.emoji_in_favor = "✅"
        self.emoji_against = "❌"
        self.delete_messages = []

    async def end_poll(self, vote_message):
        """
        execute this method if poll should end
        Args:
            vote_message: the message people are voting on
        Returns:
            None
        """
        sent_msg = await self.channel.send("Abstimmung abgeschlossen")
        self.delete_messages.append(sent_msg)
        # count votes
        votes_in_favor = 0
        votes_against = 0
        for reaction in vote_message.reactions:
            if reaction.emoji == self.emoji_in_favor:
                votes_in_favor = reaction.count - 1
            elif reaction.emoji == self.emoji_against:
                votes_against = reaction.count - 1
        # poll successful
        if votes_in_favor - votes_against >= 2:
            self.delete_messages.append(await self.channel.send("Ergebnis ist dafür."))
            await self.successful(self.member)
        else:
            self.delete_messages.append(await self.channel.send("Ergebnis ist dagegen."))
        # delete all messages
        time.sleep(3)
        for delete_msg in self.delete_messages:
            await delete_msg.delete()

    async def init_poll(self, message):
        """
        init poll, explain rules
        Returns:
            the message instance people will use to vote
        """
        rule_message = f"{message}\n Alle Benutzer haben eine Stimme, die sie innerhalb der nächsten" \
                       f" {self.time_limit} Sekunden abgeben können.\n Während dieser Zeit werden keine anderen" \
                       f" commands funktionieren."
        sent_msg = await self.channel.send(rule_message)
        self.delete_messages.append(sent_msg)
        # prepare specific message to vote
        vote_message = self.channel.last_message
        await vote_message.add_reaction(self.emoji_in_favor)
        await vote_message.add_reaction(self.emoji_against)
        return vote_message

    async def start_poll(self, message):
        """
        start poll
        Args:
            message: string message explaining the rules
        Returns:
            None
        """
        vote_message = await self.init_poll(message)
        time.sleep(self.time_limit)
        await self.end_poll(vote_message)
