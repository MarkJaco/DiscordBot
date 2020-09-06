"""
class for handling discord messages
"""
import poll
import random
import requests
import json


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
        kick_user = clean_message[len("votekick") + 1:]
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
        votekick_poll = poll.Poll(kick_member, message.channel, 10)
        # kick user from voice channel if successful
        votekick_poll.successful = lambda m: m.edit(voice_channel=None)
        # start poll
        await votekick_poll.start_poll(f"Starte votekick für {kick_user}")
        # delete user message
        await message.delete()

    async def handle_insults(self, clean_message, message):
        """
        handle all sorts of insults
        Args:
            clean_message: message command without 359!
            message: actual message object
        Returns:
            None
        """
        author_name = str(message.author)[:-5]
        # specific insults
        if clean_message == "lösch dich":
            await message.channel.send(f"lösch dich selber @{author_name}")
            return
        # lebenserfolge
        elif "in deinem leben erreicht" in clean_message:
            if message.author.permissions_in(message.channel).administrator:
                await message.channel.send("Guck mal wer redet, warst du schon mal Hamburger Meister oder kannst die Definition der Emser Depesche auswendig? Genau, NEIN")
            else:
                await message.channel.send("Guck mal wer redet, du hast ja nicht mal Rechte auf diesem Server.")
        # other insults
        comeback_list = ["Das bist du selber.", "Komm philo note Junge", "Halt die Schnauze", "Willst du Stress?",
                         "komm doch", "Willst du eine Tracht Prügel?"]
        # detect insults
        words = clean_message.split(" ")
        insult_list = ["arschloch", "hurensohn", "lappen", "fick", "dumm", "dick", "spasst", "schwul", "gay",
                       "kackspasst", "kacke", "scheisse", "scheiße"]
        for c, word in enumerate(words):
            if word in insult_list:
                if c == 0 or not ("nicht" == words[c - 1] or "kein" == words[c - 1]):
                    await message.channel.send(random.choice(comeback_list))

    async def handle_definitions(self, clean_message, message):
        """
        defines things with google api
        Args:
            clean_message: cleaned up string message
            message: message class instance
        Returns:
            None
        """
        # get word
        word = clean_message[len("definiere") + 1:]
        # get json
        source = requests.get(f"https://api.dictionaryapi.dev/api/v1/entries/de/{word}").json()
        try:
            key = list(source[0]["meaning"].keys())[0]
            definition = source[0]["meaning"][key][0]["definition"]
            await message.channel.send(f"Die Definition von {word} ist: {definition}")
        except:
            await message.channel.send(f"Gibt keine Definition für dein blödes Wort.")

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

        # real commands
        if clean_message.startswith("votekick"):
            await self.votekick(clean_message, message)

        elif "emser depesche" in clean_message:
            await message.channel.send(
                "Die Emser Depesche ist ein internes Telegramm der norddeutschen Bundesregierung vom 13. Juli 1870. Darin unterrichtete der Diplomat Heinrich Abeken den norddeutschen Bundeskanzler Otto von Bismarck in Berlin über die Vorgänge in Bad Ems. Der Bundeskanzler informierte daraufhin die Presse über die Vorgänge. Diese Pressemitteilung wird zuweilen mit der eigentlichen Depesche verwechselt, weil Bismarck großteils den Wortlaut der Depesche wiederverwendete. Die Pressemitteilung führte zu Empörung in Frankreich und gilt als ein Auslöser des Deutsch-Französischen Krieges von 1870/71. Die Depesche selbst wurde nicht veröffentlicht.")

        elif clean_message.startswith("definiere"):
            await self.handle_definitions(clean_message, message)

        elif clean_message == "hilfe":
            command_list = ["votekick [Benutzer]", "definiere [wort]"]
            await message.channel.send(f"Hier sind alle Befehle: {command_list}")

        # non commands, check for insults
        else:
            await self.handle_insults(clean_message, message)
