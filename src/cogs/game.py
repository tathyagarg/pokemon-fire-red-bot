import os
import PIL.Image
import commons
import database
from entities import data
from global_vars import *
from constants import BOT_DATA
from discord.ext import commands
from commons import check_registered
from extensions import dialogue, scene

DATABASE = BOT_DATA.DATABASE

def starting_dialogue(author_id: int) -> dialogue.Dialogue:
    return dialogue.Dialogue(
        displays=[
            (data.PROFESSOR_OAK, 'Hello, there! Glad to meet you!', None),
            (data.PROFESSOR_OAK, 'Welcome to the world of Pokémon!', None),
            (data.PROFESSOR_OAK, 'My name is Oak.', None),
            (data.PROFESSOR_OAK, 'People affectionately refer to me as the Pokémon Professor.', None),
            (data.PROFESSOR_OAK, 'This world...', None),
            (data.NIDORAN, '...is inhabited far and wide by creatures called Pokémon.', None),
            (data.NIDORAN, 'For some people, Pokémon are pets. Others use them for battling.', None),
            (data.NIDORAN, 'As for myself...', None),
            (data.NIDORAN, 'I study Pokémon as a profession.', None),
            (data.PROFESSOR_OAK, 'But first, tell me a little about yourself.', None),
            (data.PROFESSOR_OAK, 'Now tell me.', commons.Input(
                    query='Are you a boy or a girl?',
                    action=lambda gender: database.update_field(
                        uid=author_id,
                        field=DATABASE.IS_MALE,
                        new_value=gender
                    ),
                    _filter=lambda value: (first in 'mb') if (first := value[0].lower()) in 'mfbg' else True,  # True signifies male (is_male)
                    placeholder='Enter only "male", "female", "boy", or "girl"'
                )), (
                lambda: database.fetch_player_sprite(uid=author_id), 
                'Let\'s begin with your name.',
                commons.Input(
                    query='What is it?',
                    action=lambda name: database.update_field(
                        uid=author_id,
                        field=DATABASE.USERNAME,
                        new_value=name  
                    ),
                    _filter=str.title,
                    placeholder='Enter your name here.'
                )
            ), (
                lambda: database.fetch_player_sprite(uid=author_id),
                'Right... So your name is {}.',
                None
            ), 
            (data.BLUE, 'This is my grandson.', None),
            (data.BLUE, 'He\'s been your rival since you both were babies.', commons.Input(
                query='...Erm, what was his name now?',
                action=lambda name: database.update_field(
                    uid=author_id,
                    field=DATABASE.OPPONENT,
                    new_value=name
                ),
                _filter=str.title
            )),
            (data.BLUE, 'That\'s right! I remember him now! His name is {}!', None),
            (lambda: database.fetch_player_sprite(uid=author_id), lambda: f"{database.request_field(uid=author_id, field=DATABASE.USERNAME)}!", None),
            (lambda: database.fetch_player_sprite(uid=author_id), 'Your very own Pokémon legend is about to unfold!', None),
            (lambda: database.fetch_player_sprite(uid=author_id), 'A world of dreams and adventures with Pokémon awaits! Let\'s go!', None),
        ]
    )

class Game(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(check_registered)
    async def game(self, ctx: CTX) -> None:
        user_location: int = database.request_field(uid=ctx.author.id, field=DATABASE.PROGRESSION)
        if user_location == -1:
            msg: INTERACTION = await ctx.respond(embed=commons.dialogue_default_embed)
            d = starting_dialogue(author_id=ctx.author.id)
            await (await msg.original_response()).edit(view=d.paginator)
            database.update_field(uid=ctx.author.id, field=DATABASE.PROGRESSION, new_value=0)  # 0 because we know it's currently -1
            database.update_field(uid=ctx.author.id, field=DATABASE.POSITION_X, new_value=scene.SCENES[0].starting_position[0])
            database.update_field(uid=ctx.author.id, field=DATABASE.POSITION_Y, new_value=scene.SCENES[0].starting_position[1])
        else:
            uid: int = ctx.author.id

            scene_index: int = database.request_field(uid=uid, field=DATABASE.PROGRESSION)
            position: tuple[int, int] = database.request_field(uid=uid, field=DATABASE.POSITION)

            image = scene.SCENES[scene_index].image
            direction_idx: int = database.request_field(uid=uid, field=DATABASE.DIRECTION)
            direction: commons.Direction = commons.Direction.fetch(idx=direction_idx)

            user_sprite_path: str = database.fetch_player_sprite(uid=uid).overworld_sprites.from_direction(direction=direction)

            with PIL.Image.open(fp=image) as scene_img:
                with PIL.Image.open(fp=user_sprite_path) as character:
                    scene_img.paste(im=character, box=(BOT_DATA.UNITS * position[0], BOT_DATA.UNITS * position[1]), mask=character)
                    scene_img.save(f'assets/temps/{uid}.png')
            
            file: discord.File = discord.File(fp=f'assets/temps/{uid}.png', filename='output.png')
            embed = discord.Embed(color=BOT_DATA.COLORS.COLOR_PRIMARY)
            embed.set_image(url='attachment://output.png')

            await ctx.respond(embed=embed, file=file)

def setup(client: BOT) -> None:
    client.add_cog(cog=Game(bot=client))
