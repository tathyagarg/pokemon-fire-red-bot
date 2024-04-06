import discord
from global_vars import *
from typing import Callable
from commons import Character
from constants import BOT_DATA
from discord.ui import InputText

class UserModal(discord.ui.Modal):
    def __init__(self, title: str, questions: list[str]) -> None:
        super().__init__(title=title)

        self.value: list[str] = []
        self.interaction: INTERACTION = None
        self.tis: list[InputText] = [InputText(
            label=question,
            style=discord.InputTextStyle.short
        ) for question in questions]

        for ti in self.tis:
            self.add_item(item=ti)

    async def callback(self, interaction: INTERACTION) -> None:
        self.value.extend([ti.value for ti in self.tis])
        self.interaction = interaction
        self.stop()

class PaginationView(discord.ui.View):
    def __init__(self, msg_id: int, pages: list[tuple[Character, str, Callable | None]]) -> None:
        super().__init__()

        self.pages: list[tuple[Character, str, Callable | None]] = pages
        self.curr: int = -1
        self.max: int = len(pages)-1
        self.msg_id: int = msg_id

        self.disable_buttons()

    def disable_buttons(self) -> None:
        to_disable: list[str] = []
        if self.curr >= self.max:
            to_disable += ['>', '>>']
        elif self.curr <= 0:
            to_disable += ['<<', '<']

        to_disable.append('pages')

        for button in self.children:
            if button.custom_id == 'pages':
                button.label = f'{self.curr+1}/{self.max+1}'

            if button.custom_id in to_disable:
                button.disabled = True
            else:
                button.disabled = False

    @discord.ui.button(label='<<', custom_id='<<', style=discord.ButtonStyle.red)
    async def beginning(self, _, interaction: INTERACTION) -> None:
        self.curr = 0
        self.disable_buttons()

        character: Character = self.pages[self.curr][0]

        path: str = character.img
        file: discord.File = discord.File(fp=path, filename='output.png')

        embed: discord.Embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)

    @discord.ui.button(label='<', custom_id='<', style=discord.ButtonStyle.blurple)
    async def back(self, _, interaction: INTERACTION) -> None:
        self.curr -= 1
        self.disable_buttons()

        character: Character = self.pages[self.curr][0]

        path: str = character.img
        file: discord.File = discord.File(fp=path, filename='output.png')

        embed: discord.Embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)
    
    @discord.ui.button(custom_id='pages', disabled=True)
    async def _pages(self, _, interaction: INTERACTION) -> None:  # eternally disabled
        ...

    @discord.ui.button(label='>', custom_id='>', style=discord.ButtonStyle.blurple)
    async def forward(self, _, interaction: INTERACTION) -> None:
        action: Callable | None = self.pages[self.curr][2]
        result: str = ''

        if action:
            modal: UserModal = UserModal(title="What's your name?", questions=["Enter your name"])
            await interaction.response.send_modal(modal)
            _ = await modal.wait()
            result = modal.value[0]
            await modal.interaction.respond(f'You submitted {result!r}', ephemeral=True)

            action.action(result)

        self.curr += 1
        self.disable_buttons()

        character: Character = self.pages[self.curr][0]

        path: str = character.img
        file: discord.File = discord.File(fp=path, filename='output.png')

        embed: discord.Embed = discord.Embed(title=character.name, description=self.pages[self.curr][1] + result, color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        if action:
            await (await interaction.original_response()).edit(content='', embed=embed, view=self, file=file)
        else:
            await interaction.response.edit_message(content='', embed=embed, view=self, file=file)

    @discord.ui.button(label='>>', custom_id='>>', style=discord.ButtonStyle.green)
    async def end(self, _, interaction: INTERACTION) -> None:
        self.curr = self.max
        self.disable_buttons()

        character: Character = self.pages[self.curr][0]

        path: str = character.img
        file: discord.File = discord.File(fp=path, filename='output.png')

        embed: discord.Embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)


class Dialogue:
    def __init__(self, msg_id: int, displays: list[tuple[Character, str, Callable | None]]) -> None:
        self.msg_id: int = msg_id
        self.displays: list[tuple[Character, str, Callable | None]] = displays

    @property
    def paginator(self) -> PaginationView:
        return PaginationView(msg_id=self.msg_id, pages=self.displays)
