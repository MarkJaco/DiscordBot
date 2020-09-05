"""
this module handles Polls

for example kicking someone from a voice channel
"""
import time


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

    async def end_poll(self, vote_message):
        """
        execute this method if poll should end
        Args:
            vote_message: the message people are voting on
        Returns:
            None
        """
        await self.channel.send(f"Abstimmung abgeschlossen")
        # count votes
        votes_in_favor = 0
        votes_against = 0
        for reaction in vote_message.reactions:
            if reaction.emoji == self.emoji_in_favor:
                votes_in_favor = reaction.count - 1
            elif reaction.emoji == self.emoji_against:
                votes_against = reaction.count - 1
        print("votes in favor ", votes_in_favor)
        print("votes against ", votes_against)
        # poll successful
        if votes_in_favor - votes_against >= 2:
            await self.channel.send("Ergebnis ist dafür")
            await self.successful(self.member)
        else:
            await self.channel.send("Ergebnis ist dagegen")

    async def init_poll(self, message):
        """
        init poll, explain rules
        Returns:
            the message instance people will use to vote
        """
        await self.channel.send(message)
        await self.channel.send(f"Alle Benutzer haben eine Stimme, die sie innerhalb der nächsten {self.time_limit} Sekunden abgeben können.")
        await self.channel.send("Während dieser Zeit werden keine anderen commands funktionieren.")
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
