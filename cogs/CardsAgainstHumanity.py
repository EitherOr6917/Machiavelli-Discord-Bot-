# Import statements
import asyncio
from other.CommonBotFunctions import *
import random


class CardsAgainstHumanity(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['cardsagainsthumanity', 'cah'], help='Cards Against Humanity')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cards_against_humanity(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send('WORK IN PROGRESS COMMAND: Do you wish to proceed (y/n)?')
            while True:
                try:
                    msg = await self.client.wait_for(
                        'message',
                        check=lambda message: message.author == ctx.author, timeout=90
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f'Sorry {ctx.author.display_name}, your command has timed out.')
                else:
                    if ('n' not in msg.content.lower()) and ('y' not in msg.content.lower()):
                        await ctx.send('Please respond with \'y\' or \'n\'.')
                    else:
                        if 'n' in msg.content.lower():
                            await ctx.send('Exiting')
                            return
                        if 'y' in msg.content.lower():
                            await ctx.send('Continuing')
                            break

            # Initiate the game
            players = [ctx.author]
            for user in ctx.message.mentions:
                players.append(user)

            check_message = 'Players: '
            for user in players:
                if user != players[-1]:
                    check_message += ', '
                if user == players[-1]:
                    check_message += 'and '
                check_message += user.display_name
            check_message += '. Confirm (y/n):'

            await ctx.send(check_message)

            while True:
                try:
                    msg = await self.client.wait_for(
                        'message',
                        check=lambda message: message.author == ctx.author, timeout=90
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f'Sorry {ctx.author.display_name}, your command has timed out.')
                else:
                    if 'y' not in msg.content.lower() and 'n' not in msg.content.lower():
                        await ctx.send('Please respond with \'yes\' or \'no\'.')
                    else:
                        if 'n' in msg.content.lower():
                            await ctx.send('Command canceled, please restart!')
                            return
                        elif 'y' in msg.content.lower():
                            break

            # Ask whether or not to use text to speech
            cah_tts = False
            await ctx.send('Use /tts for messages (y/n)?')
            replied_correctly = False
            while True:
                try:
                    msg = await self.client.wait_for(
                        'message',
                        check=lambda message: message.author == ctx.author, timeout=90
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f'Sorry {ctx.author.display_name}, your command has timed out.')
                else:
                    if ('y' and 'n' not in msg.content.lower()) or ('y' and 'n' in msg.content.lower()):
                        await ctx.send('Please respond with \'yes\' or \'no\'.')
                    else:
                        if 'n' in msg.content.lower():
                            await ctx.send('Text to speech off!')
                            break
                        elif 'y' in msg.content.lower():
                            await ctx.send('Text to speech on!')
                            cah_tts = True
                            break

            # Now for the actual game
            await ctx.send('At the end of each round, current points will be displayed and you may end the game.')

            with open('jsons/cahcards.json', 'r') as file:
                cards = json.load(file)
            discard_pile = {
                'white': [],
                'black': []
            }
            game_data = {}
            for player in players:
                game_data[player.id] = {
                    'cards': [],
                    'points': 0
                }

            game_round = 0
            random.shuffle(players)
            while True:  # Start game loop
                await ctx.send(f'Round {game_round}:', tts=cah_tts)
                # Choosing Card Tsar
                card_czar = players[game_round % len(players)]
                # Distribute hands
                random.shuffle(cards['black'])
                random.shuffle(cards['white'])
                for player in players:
                    while len(game_data[player.id]['hand']) < 10:
                        top_card = cards['white'].pop()
                        game_data[player.id]['hand'].append(top_card)
                # Say round info
                round_card = cards['black'].pop()
                await ctx.send(f'The Card Czar this round is {card_czar.display_name}, and the card is:\n'
                               f'**{round_card}**', tts=cah_tts)


    @commands.command(aliases=['cardsagainsthumanityrules', 'cahrules'], help='Cards Against Humanity Rules')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cards_against_humanity_rules(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.author.send('To start the game, each player draws ten white cards. \nThe player who most '
                                  'recently pooped begins as the Card Czar and draws a black card. If Hugh '
                                  'Jackman is playing, he goes first, regardless of how recently he pooped. \nThe '
                                  'Card Czar reads the question or fill-in-the-blank phrase on the black card out '
                                  'loud. Everyone else answers the question or fills in the blank by passing one '
                                  'white card, face down, to the Card Czar. \nThe Card Czar then shuffles all the '
                                  'answers and reads each card combination out loud to the group. The Card Czar '
                                  'should re-read the black card before presenting each answer. Finally, '
                                  'the Card Czar picks the funniest play, and whoever submitted it gets one '
                                  'point. \nAfter the round, a new player becomes the Card Czar and everyone draws '
                                  'back up to ten white cards')


def setup(client):
    client.add_cog(CardsAgainstHumanity(client))
