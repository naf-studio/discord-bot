"""Administrative slash commands for guild management, announcements, and tree sync."""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from discord_bot.config import Settings

logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    """Cog providing privileged administrative interactions and maintenance utilities."""

    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        self.bot = bot
        self.settings = settings

    def _get_template(self, name: str) -> str | None:
        file_path = self.settings.messages_dir / f"{name}.txt"
        if file_path.is_file():
            return file_path.read_text(encoding="utf-8")
        return None

    def _list_templates(self) -> list[str]:
        if not self.settings.messages_dir.is_dir():
            return []
        return [f.stem for f in self.settings.messages_dir.glob("*.txt") if f.is_file()]

    @app_commands.command(
        name="sync",
        description="Synchronize application commands with Discord API.",
    )
    @app_commands.describe(
        scope="Target synchronization scope: 'guild' (instant) or 'global' (up to 1hr)",
    )
    @app_commands.choices(
        scope=[
            app_commands.Choice(name="Current Guild", value="guild"),
            app_commands.Choice(name="Global", value="global"),
        ]
    )
    @app_commands.default_permissions(administrator=True)
    async def sync_tree(
        self,
        interaction: discord.Interaction,
        scope: str = "guild",
    ) -> None:
        """Manually trigger application command registration."""
        await interaction.response.defer(ephemeral=True)

        if scope == "guild":
            if not interaction.guild:
                await interaction.followup.send(
                    "Guild scope can only be synchronized inside a server.",
                    ephemeral=True,
                )
                return
            self.bot.tree.copy_global_to(guild=interaction.guild)
            synced = await self.bot.tree.sync(guild=interaction.guild)
            await interaction.followup.send(
                f"Successfully synced {len(synced)} command(s) to this guild.",
                ephemeral=True,
            )
        else:
            synced = await self.bot.tree.sync()
            await interaction.followup.send(
                f"Successfully initiated global sync for {len(synced)} command(s).",
                ephemeral=True,
            )

    @app_commands.command(
        name="msg",
        description="Dispatch a direct message to a designated user.",
    )
    @app_commands.describe(
        user="Target user to receive direct message",
        content="Raw text message or template file name without extension",
    )
    @app_commands.default_permissions(administrator=True)
    async def msg(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        content: str,
    ) -> None:
        """Send a direct message using template or inline text."""
        template_content = self._get_template(content)
        final_message = (
            template_content
            if template_content is not None
            else content.replace("\\n", "\n")
        )

        try:
            await user.send(final_message)
            await interaction.response.send_message(
                f"Dispatched message to {user.mention}.",
                ephemeral=True,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"Unable to reach {user.mention}. Direct messages might be disabled.",
                ephemeral=True,
            )
        except discord.HTTPException as exc:
            logger.error("Failed to deliver message to user %s: %s", user.id, exc)
            await interaction.response.send_message(
                "An unexpected HTTP error occurred while sending the message.",
                ephemeral=True,
            )

    @app_commands.command(
        name="broadcast",
        description="Broadcast the template announcement to all guild members.",
    )
    @app_commands.default_permissions(administrator=True)
    async def broadcast(self, interaction: discord.Interaction) -> None:
        """Deliver broadcast template message to all non-bot members in guild."""
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message(
                "Command can only be executed inside a guild.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        message_content = self._get_template("broadcast")
        if not message_content:
            await interaction.followup.send(
                f"Announcement template not found at `{self.settings.messages_dir / 'broadcast.txt'}`.",
                ephemeral=True,
            )
            return

        undelivered: list[str] = []
        for member in guild.members:
            if member.bot:
                continue
            try:
                await member.send(message_content)
            except (discord.Forbidden, discord.HTTPException):
                undelivered.append(member.display_name)

        if undelivered:
            preview = ", ".join(undelivered[:10])
            extra = (
                f" (and {len(undelivered) - 10} others)"
                if len(undelivered) > 10
                else ""
            )
            await interaction.followup.send(
                f"Broadcast completed. Undelivered to {len(undelivered)} members: {preview}{extra}.",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                "Broadcast successfully delivered to all members.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot) -> None:
    """Register AdminCog with the bot instance."""
    settings = getattr(bot, "settings", Settings(bot_token="placeholder"))
    await bot.add_cog(AdminCog(bot, settings))
