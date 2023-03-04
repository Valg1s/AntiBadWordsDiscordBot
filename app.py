import os
import re


import discord
from dotenv import load_dotenv

from parse import serialize, deserialize


class MyClient(discord.Client):
    bad_words = None

    async def on_ready(self):
        MyClient.bad_words = deserialize()

    async def on_message(self, message):
        # don't respond to ourselves
        print(message.content)
        if message.author == self.user:
            return

        message_text = map(lambda x: x.lower(),re.findall(r"[\d|\w]+", message.content))

        for word in message_text:
            bad_words_on_letter = MyClient.bad_words.get(word[0],None)

            if bad_words_on_letter:
                if word in bad_words_on_letter:
                    await message.delete()

                else:
                    for bad_word in bad_words_on_letter:
                        if bad_word in word:
                            await message.delete()

                        elif word in bad_word:
                            print(f"Слово юзера:{word} -- Підозра на слово: {bad_word}: {len(word)} / {len(bad_word)}"
                                  f" = {len(word) / len(bad_word) >= 0.8}")
                            if len(word) / len(bad_word) >= 0.8:
                                await message.delete()


        '''if message.content == 'ping':
            await message.channel.send('pong')'''


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv('DISCORD_GUILD')

    client.run(DISCORD_TOKEN)