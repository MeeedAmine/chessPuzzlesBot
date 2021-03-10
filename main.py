import discord
from chessdotcom import get_current_daily_puzzle, get_random_daily_puzzle
import io
import aiohttp
import chess.pgn
import json

with open('token.json') as f:
    TOKEN = json.load(f)['token']

client = discord.Client()



def get_solution(pgn):
    solution = pgn.split('\r\n')[-1]
    if solution == '*':
        solution = pgn.split('\r\n')[-2]
    return solution

def get_turn(pgn):
    pgn = io.StringIO(pgn)
    game = chess.pgn.read_game(pgn)
    if game.turn():
        return 'White to move.'
    else:
        return 'Black to move.'

def daily_puzzle():
    data = get_current_daily_puzzle().json
    pgn = data['pgn']
    titel = data['title']
    image_url = data['image']
    solution = get_solution(pgn)
    return titel, image_url, solution

def random_puzzle():
    data = get_random_daily_puzzle().json
    pgn = data['pgn']
    turn = get_turn(pgn)
    title = data['title']
    image_url = data['image']
    solution = get_solution(pgn)
    return title, turn, image_url, solution

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$puzzle'):
        global solution
        title, turn, image_url, solution = random_puzzle()
        await message.channel.send(f'{title}. {turn}')
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, f'{title}.png'))
                await message.channel.send(f'Solution (First, try to solve it by your self!): ||{solution}||')
                
    if message.content.startswith('$s'):
        if solution:
            await message.channel.send(f'Solution: ||{solution}||')




client.run(TOKEN)


#TODO find a way to add a frame for the coordinates of the board (svg to png!!!)