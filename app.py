import os
import re
import difflib


import discord
from discord.ext import commands
from dotenv import load_dotenv

from parse import serialize, deserialize, _to_default


class MyClient(discord.Client):
    bad_words = None
    exceptions = None

    async def on_ready(self):
        MyClient.bad_words = deserialize(mode="bad_words")
        MyClient.exceptions = deserialize(mode="exceptions")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.author.name == "Valg1s" and message.content == "Люк,я твой отец":
            await message.channel.send("Здравствуйте,мой хозяин и создатель,Антон!")

        if message.author.name == "Valg1s" and message.content == "/reset_to_default":
            _to_default()

        if "Адміністратор" in [role.name for role in message.author.roles]:
            if message.content.startswith('/add_bad_word'):
                word = message.content.split(" ")[1:]

                if len(word) != 1:
                    await message.delete()
                    await message.channel.send("Введіть лише одне слово.")

                else:
                    word = word[0]

                    bad_word_on_letter = MyClient.bad_words.get(word[0],None)

                    if bad_word_on_letter:
                        if word not in bad_word_on_letter:
                            bad_word_on_letter.append(word)

                    else:
                        bad_word_on_letter[word[0]] = [word]

                    serialize(word, mode="bad_words")

                    await message.delete()

            if message.content.startswith('/add_exception'):
                word = message.content.split(" ")[1:]

                if len(word) != 1:
                    await message.delete()
                    await message.channel.send("Введіть лише одне слово.")

                else:
                    word = word[0]
                    if word not in MyClient.exceptions:
                        MyClient.exceptions.append(word)

                        serialize(word, mode="exceptions")

                    await message.delete()

        message_text = map(lambda x: x.lower(), re.findall(r"[\d|\w]+", message.content))

        for word in message_text:
            if word not in MyClient.exceptions:
                bad_words_on_letter = MyClient.bad_words.get(word[0],None)

                if bad_words_on_letter:
                    if word in bad_words_on_letter:
                        await message.delete()

                    else:
                        for bad_word in bad_words_on_letter:
                            mather = difflib.SequenceMatcher(None,word,bad_word)

                            if mather.ratio() >= 0.8:
                                await message.delete()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv('DISCORD_GUILD')

    client.run(DISCORD_TOKEN)
