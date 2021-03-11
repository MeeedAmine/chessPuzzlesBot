import discord
from discord.ext import commands, tasks
from chessdotcom import get_current_daily_puzzle, get_random_daily_puzzle
import io
import aiohttp
import chess.pgn
import json



with open('token.json') as f:
    TOKEN = json.load(f)['token']


bot = commands.Bot(command_prefix="!")


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
    turn = get_turn(pgn)
    titel = data['title']
    image_url = data['image']
    solution = get_solution(pgn)
    return titel, turn, image_url, solution

def random_puzzle():
    data = get_random_daily_puzzle().json
    pgn = data['pgn']
    turn = get_turn(pgn)
    title = data['title']
    image_url = data['image']
    solution = get_solution(pgn)
    return title, turn, image_url, solution

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(
    name = 'daily_puzzle',
    help="Type the above command to enjoy the puzzle of this day;)",
	brief="Gives you the puzzle of today from chess.com with its solution"
    )
async def daillypuzzle(ctx):
    title, turn, image_url, solution = daily_puzzle()
    await ctx.channel.send(f'{title}. {turn}')
    async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.channel.send('Could not download the puzzle, wait and try again!')
                data = io.BytesIO(await resp.read())
                await ctx.channel.send(file=discord.File(data, f'{title}.png'))
                await ctx.channel.send(f'Solution (First, try to solve it by your self!): ||{solution}||')

@bot.command(
    name = 'puzzle',
    help="Type the above command to enjoy the puzzles ;)",
	brief="Gives you a random puzzle from chess.com with its solution"
    )
async def puzzle(ctx):
    title, turn, image_url, solution = random_puzzle()
    await ctx.channel.send(f'{title}. {turn}')
    async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await ctx.channel.send('Could not download the puzzle, wait and try again!')
                data = io.BytesIO(await resp.read())
                await ctx.channel.send(file=discord.File(data, f'{title}.png'))
                await ctx.channel.send(f'Solution (First, try to solve it by your self!): ||{solution}||')





bot.run(TOKEN)


#TODO find a way to add a frame for the coordinates of the board (svg to png!!!)