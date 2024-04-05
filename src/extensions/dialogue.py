import discord
from typing import Callable
from discord.ui import InputText
from commons import Character
from constants import BOT_DATA

class UserModal(discord.ui.Modal):
    def __init__(self, title, questions) -> None:
        super().__init__(title=title)

        self.value = []
        self.interaction = None
        self.tis = [InputText(
            label=question,
            style=discord.InputTextStyle.short
        ) for question in questions]

        for ti in self.tis:
            self.add_item(ti)

    async def callback(self, interaction: discord.Interaction):
        self.value.extend([ti.value for ti in self.tis])
        self.interaction = interaction
        self.stop()

class PaginationView(discord.ui.View):
    def __init__(self, msg_id, pages):
        super().__init__()

        self.pages = pages
        self.curr = -1
        self.max = len(pages)-1
        self.msg_id = msg_id

        self.disable_buttons()

    def disable_buttons(self):
        if self.curr >= self.max:
            to_disable = ['>', '>>']
        elif self.curr <= 0:
            to_disable = ['<<', '<']
        else:
            to_disable = []
        to_disable.append('pages')

        for button in self.children:
            if button.custom_id == 'pages':
                button.label = f'{self.curr+1}/{self.max+1}'

            if button.custom_id in to_disable:
                button.disabled = True
            else:
                button.disabled = False

    @discord.ui.button(label='<<', custom_id='<<', style=discord.ButtonStyle.red)
    async def beginning(self, button, interaction):
        self.curr = 0
        self.disable_buttons()

        character = self.pages[self.curr][0]

        path = character.img
        file = discord.File(path, filename='output.png')

        embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)

    @discord.ui.button(label='<', custom_id='<', style=discord.ButtonStyle.blurple)
    async def back(self, button, interaction):
        self.curr -= 1
        self.disable_buttons()

        character = self.pages[self.curr][0]

        path = character.img
        file = discord.File(path, filename='output.png')

        embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)
    
    @discord.ui.button(custom_id='pages', disabled=True)
    async def _pages(self, button, interaction):  # eternally disabled
        ...

    @discord.ui.button(label='>', custom_id='>', style=discord.ButtonStyle.blurple)
    async def forward(self, button, interaction):
        action = self.pages[self.curr][2]
        result = ''

        if action:
            modal = UserModal(title="What's your name?", questions=["Enter your name"])
            await interaction.response.send_modal(modal)
            _ = await modal.wait()
            result = modal.value[0]
            await modal.interaction.respond(f'You submitted {result!r}', ephemeral=True)

            action.action(result)

        self.curr += 1
        self.disable_buttons()

        character = self.pages[self.curr][0]

        path = character.img
        file = discord.File(path, filename='output.png')

        embed = discord.Embed(title=character.name, description=self.pages[self.curr][1] + result, color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        if action:
            await (await interaction.original_response()).edit(content='', embed=embed, view=self, file=file)
        else:
            await interaction.response.edit_message(content='', embed=embed, view=self, file=file)

    @discord.ui.button(label='>>', custom_id='>>', style=discord.ButtonStyle.green)
    async def end(self, button, interaction):
        self.curr = self.max
        self.disable_buttons()

        character = self.pages[self.curr][0]

        path = character.img
        file = discord.File(path, filename='output.png')

        embed = discord.Embed(title=character.name, description=self.pages[self.curr][1], color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        await interaction.response.edit_message(content='', embed=embed, view=self, file=file)


class Dialogue:
    def __init__(self, msg_id: int, displays: list[tuple[Character, str, Callable | None]]) -> None:
        self.msg_id = msg_id
        self.displays = displays

    @property
    def paginator(self):
        return PaginationView(self.msg_id, self.displays)
