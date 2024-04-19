import PIL
import commons
import discord
import database
from extensions import scenes
from commons import INTERACTION
from constants import BOT_DATA

PRE_GAME_EMBED = discord.Embed(
    title='The game is about to start!',
    description='Get ready!',
    color=BOT_DATA.COLORS.COLOR_PRIMARY
)

DATABASE = BOT_DATA.DATABASE

def make_image(uid: int) -> str:
    scene_index: int = database.request_field(uid=uid, field=DATABASE.PROGRESSION)
    position: tuple[int, int] = database.request_field(uid=uid, field=DATABASE.POSITION)

    image = scenes.SCENES[scene_index].image
    direction_idx: int = database.request_field(uid=uid, field=DATABASE.DIRECTION)
    direction: commons.Direction = commons.Direction.fetch(idx=direction_idx)

    user_sprite_path: str = database.fetch_player_sprite(uid=uid).overworld_sprites.from_direction(direction=direction)

    with PIL.Image.open(fp=image) as scene_img:
        with PIL.Image.open(fp=user_sprite_path) as character:
            scene_img.paste(im=character, box=(BOT_DATA.UNITS * position[0], BOT_DATA.UNITS * position[1]), mask=character)
            fname: str = f'assets/temps/{uid}.png'

            scene_img.save(fname)
    
    return fname

def check_can_move(uid: int, direction: commons.Direction) -> bool:
    x, y = database.request_field(uid=uid, field=DATABASE.POSITION)
    scene_idx = database.request_field(uid=uid, field=DATABASE.PROGRESSION)

    scene = scenes.SCENES[scene_idx]

    return (x, y, direction) not in scene.walls

class GameEmbed(discord.Embed):
    def __init__(self, uid: int) -> None:
        fname: str = make_image(uid=uid)
        self.file = discord.File(fname, filename='output.png')

        super().__init__(color=BOT_DATA.COLORS.COLOR_PRIMARY)
        self.set_image(url='attachment://output.png')

class GameView(discord.ui.View):
    def __init__(self, uid: int):
        super().__init__()

        self.embed: GameEmbed = None
        self.uid = uid

    @discord.ui.button(label='ㅤ', row=0)
    async def filler1(self, _, __): ...

    @discord.ui.button(emoji='⬆️', style=discord.ButtonStyle.green, row=0)
    async def up(self, _, interaction: INTERACTION):
        if check_can_move(uid=self.uid, direction=commons.Direction.BACK):
            database.update_field(uid=self.uid, field=DATABASE.POSITION_Y, new_value=database.request_field(uid=self.uid, field=DATABASE.POSITION_Y)-1)
        database.update_field(uid=self.uid, field=DATABASE.DIRECTION, new_value=commons.Direction.BACK.value)
        fname: str = make_image(uid=self.uid)

        file = discord.File(fname, filename='output.png')
        self.embed.file = file
        await interaction.response.edit_message(embed=self.embed, file=file)

    @discord.ui.button(label='ㅤ', row=0)
    async def filler2(self, _, __): ...

    @discord.ui.button(label='ㅤ', row=0)
    async def filler3(self, _, __): ...

    @discord.ui.button(label='ㅤ', row=0)
    async def filler4(self, _, __): ...

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green, row=1)
    async def left(self, _, interaction: INTERACTION):
        if check_can_move(uid=self.uid, direction=commons.Direction.LEFT):
            database.update_field(uid=self.uid, field=DATABASE.POSITION_X, new_value=database.request_field(uid=self.uid, field=DATABASE.POSITION_X)-1)
        database.update_field(uid=self.uid, field=DATABASE.DIRECTION, new_value=commons.Direction.LEFT.value)
        fname: str = make_image(uid=self.uid)

        file = discord.File(fname, filename='output.png')
        self.embed.file = file
        await interaction.response.edit_message(embed=self.embed, file=file)

    @discord.ui.button(label='ㅤ', row=1)
    async def filler5(self, _, __): ...

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green, row=1)
    async def right(self, _, interaction: INTERACTION):
        if check_can_move(uid=self.uid, direction=commons.Direction.RIGHT):
            database.update_field(uid=self.uid, field=DATABASE.POSITION_X, new_value=database.request_field(uid=self.uid, field=DATABASE.POSITION_X)+1)
        database.update_field(uid=self.uid, field=DATABASE.DIRECTION, new_value=commons.Direction.RIGHT.value)
        fname: str = make_image(uid=self.uid)

        file = discord.File(fname, filename='output.png')
        self.embed.file = file
        await interaction.response.edit_message(embed=self.embed, file=file)

    @discord.ui.button(label='A', style=discord.ButtonStyle.blurple, row=1)
    async def button_a(self, _, __): ...

    @discord.ui.button(label='B', style=discord.ButtonStyle.blurple, row=1)
    async def button_b(self, _, __): ...

    @discord.ui.button(label='ㅤ', row=2)
    async def filler6(self, _, __): ...

    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.green, row=2)
    async def down(self, _, interaction: INTERACTION):
        if check_can_move(uid=self.uid, direction=commons.Direction.FRONT):
            database.update_field(uid=self.uid, field=DATABASE.POSITION_Y, new_value=database.request_field(uid=self.uid, field=DATABASE.POSITION_Y)+1)
        database.update_field(uid=self.uid, field=DATABASE.DIRECTION, new_value=commons.Direction.FRONT.value)
        fname: str = make_image(uid=self.uid)

        file = discord.File(fname, filename='output.png')
        self.embed.file = file
        await interaction.response.edit_message(embed=self.embed, file=file)

    @discord.ui.button(label='ㅤ', row=2)
    async def filler7(self, _, __): ...

    @discord.ui.button(label='ㅤ', row=2)
    async def filler8(self, _, __): ...

    @discord.ui.button(label='End Interaction', style=discord.ButtonStyle.red, row=2)
    async def end_interaction(self, _, interaction: INTERACTION):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
