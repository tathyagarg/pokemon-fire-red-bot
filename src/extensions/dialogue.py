import discord
from commons import Input
from global_vars import *
from typing import Callable
from commons import Character
from constants import BOT_DATA
from discord.ui import InputText

class UserModal(discord.ui.Modal):
    def __init__(self, title: str, question: str, placeholder: str) -> None:
        super().__init__(title=title)

        self.value: str = None
        self.interaction: INTERACTION = None
        self.ti: InputText = InputText(
            label=question,
            style=discord.InputTextStyle.short,
            placeholder=placeholder
        )

        self.add_item(item=self.ti)

    async def callback(self, interaction: INTERACTION) -> None:
        self.value = self.ti.value
        self.interaction = interaction
        self.stop()

class PaginationView(discord.ui.View):
    def __init__(self, pages: list[tuple[Character, str, Callable | None]]) -> None:
        super().__init__()

        self.pages: list[tuple[Character, str, Callable | None]] = pages
        self.curr: int = 0
        self.max: int = len(pages)-1

        self.disable_buttons()

    def disable_buttons(self) -> None:
        to_disable: list[str] = ['pages', 'destroy']
        if self.curr >= self.max:
            to_disable += ['>']
            to_disable.remove('destroy')

        for button in self.children:
            if button.custom_id == 'pages':
                button.label = f'{self.curr+1}/{self.max+1}'

            if button.custom_id in to_disable:
                button.disabled = True
            else:
                button.disabled = False

    @discord.ui.button(custom_id='pages', disabled=True)
    async def _pages(self, _, interaction: INTERACTION) -> None:  # eternally disabled
        ...

    @discord.ui.button(label='>', custom_id='>', style=discord.ButtonStyle.blurple)
    async def forward(self, _, interaction: INTERACTION) -> None:
        action: Input | None = self.pages[self.curr][2]
        result: str = ''

        if action:
            modal: UserModal = UserModal(title='Query', question=action.query, placeholder=action.placeholder)
            await interaction.response.send_modal(modal)
            _ = await modal.wait()
            result = action._filter(modal.value)
            await modal.interaction.respond(f'Your input has been processed.', ephemeral=True)

            action.action(result)

        self.curr += 1
        self.disable_buttons()

        character: Character = self.pages[self.curr][0]
        try:
            character = character()
        except TypeError:
            pass

        text = self.pages[self.curr][1]
        try:
            text = text()
        except TypeError:
            pass

        path: str = character.img
        file: discord.File = discord.File(fp=path, filename='output.png')

        embed: discord.Embed = discord.Embed(title='Dialogue', description=text.format(result), color=BOT_DATA.COLORS.COLOR_PRIMARY)
        embed.set_image(url=f'attachment://output.png')

        if action:
            await (await interaction.original_response()).edit(content='', embed=embed, view=self, file=file)
        else:
            await interaction.response.edit_message(content='', embed=embed, view=self, file=file)

class Dialogue:
    def __init__(self, msg_id: int, displays: list[tuple[Character, str, Callable | None]]) -> None:
        self.msg_id = msg_id
        self.displays = displays
        self.paginator = PaginationView(pages=self.displays)
