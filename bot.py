import gc
import threading
from importlib import reload

from commands.send_to_channel import between_callback

from twitchio.ext import commands
import time
from models.config import CHANNELS, TMI_TOKEN, CLIENT_ID, BOT_NICK, BOT_PREFIX

from models.data import Message
from models.constants import IGNORES, GENIUS, DISCORD
from models.statistic import save_statistic, load_statistic

HELLO = 'KonCha'


stats = Message('stats', 'Statistics', [], 60)
discord = Message('ds', 'discord', [DISCORD], 60, wait_before=10)
genius = Message('genius', "Genius", [GENIUS], 60, wait_before=1)

bot = commands.Bot(
    # set up the bot
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNELS
)


@bot.event
async def event_ready():
    """Called once when the bot goes online."""
    objects = _get_all_objects()

    ws = bot._ws
    await ws.send_privmsg(CHANNELS[0], HELLO)
    

    _stats_load_thread = threading.Thread(target=load_statistic, args=(objects,))
    _stats_load_thread.start()

    _stats_save_thread = threading.Thread(target=save_statistic, args=(objects,))
    _stats_save_thread.start()


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    print('> ', ctx.author.name,  ctx.content)

    await bot.handle_commands(ctx)

    # Statistic message
    if ctx.content.lower().startswith('@' + BOT_NICK.lower()) and 'stats' in ctx.content:
        stats_message = _get_statistic()
        stats.messages = [stats_message]
        await send_to_channel(ctx, stats)


@bot.command(name='ds', aliases=['discord', 'дискорд', 'дс'])
async def test(ctx):
    await send_to_channel(ctx, discord)


@bot.command(name='гений')
async def test(ctx):
    await send_to_channel(ctx, genius)


@bot.command(name='iq', aliases=IGNORES)
async def test(ctx):
    return True

# Additional functions
def _get_statistic():
    commands_list = _get_all_objects()
    response = ''

    for command in commands_list:
        message = " {}:{}|".format(command.name, command.calls)
        print(message)
        response += message

    return response


async def send_to_channel(ctx, command_object):
    '''
    Send command to channel and create awaitng thread
    :param ctx: bot object with channel
    :param command_object: response object
    :return: nothing
    '''
    if command_object.usage == 0:
        author = '@' + ctx.author.name
        await ctx.channel.send(command_object.messages[0].replace('-AUTHOR-', author))
        command_object.usage += 1
        command_object.calls += 1
        if command_object.sleep != 0:
            x = threading.Thread(target=clean_up_usage, args=(command_object,))
            x.start()
    else:
        command_object.skips += 1
        print('SKIPING by usage timeout: {}'.format(command_object.messages[0]))


def clean_up_usage(command_object):
    time.sleep(command_object.sleep)
    command_object.usage = 0


def _get_current_game():
    reload(dinamyc)
    response = dinamyc.game()
    return response


def _get_all_objects():
    commands_list = []
    for obj in gc.get_objects():
        if isinstance(obj, Message):
            commands_list.append(obj)
    return commands_list


if __name__ == '__main__':
    bot.run()
