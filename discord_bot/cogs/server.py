"""Community information and Minecraft server lookup slash commands."""

import discord
from discord import app_commands
from discord.ext import commands

from discord_bot.config import Settings

SMP_CHANNEL_URL = "https://discord.com/channels/998500551488708618/1129023879105499177/1130148231553241092"
MINIGAME_CHANNEL_URL = "https://discord.com/channels/998500551488708618/1267736839976910951/1272413804709412905"


class ServerCog(commands.Cog):
    """Cog handling server connection details and community documentation links."""

    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        self.bot = bot
        self.settings = settings

    @app_commands.command(
        name="ip",
        description="Obtain connection address and guide for Minecraft servers.",
    )
    @app_commands.describe(which_server="Select destination server: SMP or MINIGAME")
    @app_commands.choices(
        which_server=[
            app_commands.Choice(name="SMP", value="smp"),
            app_commands.Choice(name="MINIGAME", value="minigame"),
        ]
    )
    async def ip(
        self,
        interaction: discord.Interaction,
        which_server: str = "smp",
    ) -> None:
        """Provide destination-specific connection guide link."""
        target_url = SMP_CHANNEL_URL if which_server == "smp" else MINIGAME_CHANNEL_URL
        await interaction.response.send_message(f"-> {target_url}")

    @app_commands.command(
        name="smp",
        description="Quick access to SMP server connection instructions.",
    )
    async def smp(self, interaction: discord.Interaction) -> None:
        """Shortcut command for SMP connection."""
        await interaction.response.send_message(f"-> {SMP_CHANNEL_URL}")

    @app_commands.command(
        name="minigame",
        description="Quick access to Minigame server connection instructions.",
    )
    async def minigame(self, interaction: discord.Interaction) -> None:
        """Shortcut command for Minigame connection."""
        await interaction.response.send_message(f"-> {MINIGAME_CHANNEL_URL}")

    @app_commands.command(
        name="discord",
        description="Retrieve community Discord invite link.",
    )
    async def discord_link(self, interaction: discord.Interaction) -> None:
        """Send current public server invite URL."""
        await interaction.response.send_message(
            f"-> {self.settings.discord_invite_link}"
        )

    @app_commands.command(
        name="help",
        description="List all available application commands.",
    )
    async def help_command(self, interaction: discord.Interaction) -> None:
        """Display an organized embed summary of registered slash commands."""
        embed = discord.Embed(
            title="Available Slash Commands",
            color=discord.Color.blurple(),
        )
        for command in self.bot.tree.get_commands():
            if isinstance(command, (app_commands.Command, app_commands.Group)):
                description = command.description or "No description provided."
            else:
                description = "Context menu command."

            embed.add_field(
                name=f"/{command.name}",
                value=description,
                inline=False,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Register ServerCog with the bot instance."""
    settings = getattr(bot, "settings", Settings(bot_token="placeholder"))
    await bot.add_cog(ServerCog(bot, settings))
