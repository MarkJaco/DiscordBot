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
        self.votes_in_favor = 0
        self.votes_against = 0
        self.members_voted = []

    async def end_poll(self):
        """
        execute this method if poll should end
        Returns:
            None
        """
        await self.channel.send(f"Abstimmung abgeschlossen")
        # poll successful
        if self.votes_in_favor - self.votes_against >= 3:
            await self.channel.send("Ergebnis ist dafür")
            self.successful(self.member)
        else:
            await self.channel.send("Ergebnis ist dafür")

    async def init_poll(self, message):
        """
        init poll, explain rules
        Returns:
            None
        """
        await self.channel.send(message)
        await self.channel.send(f"'359! f1' steht für dafür und '359! f2' steht für dagegen.")
        await self.channel.send(f"Alle Benutzer haben eine Stimme, die sie innerhalb der nächsten {self.time_limit} Sekunden abgeben können.")
        await self.channel.send("Während dieser Zeit werden keine anderen commands funktionieren.")

    async def start_poll(self, message):
        """
        start poll
        Args:
            message: string message explaining the rules
        Returns:
            None
        """
        await self.init_poll(message)
        time.sleep(self.time_limit)
        await self.end_poll()
