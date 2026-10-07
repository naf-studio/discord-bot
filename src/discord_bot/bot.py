"""Discord bot client initialization, error handling, and lifecycle orchestration."""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from discord_bot.config import Settings

logger = logging.getLogger(__name__)

INITIAL_EXTENSIONS = (
    "discord_bot.cogs.admin",
    "discord_bot.cogs.server",
    "discord_bot.cogs.events",
)


async def handle_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
) -> None:
    """Provide structured, user-friendly responses for unhandled interaction errors."""
    if isinstance(error, app_commands.MissingPermissions):
        message = "You do not have the required permissions to execute this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        message = "The bot lacks required server permissions to complete this action."
    elif isinstance(error, app_commands.CommandOnCooldown):
        message = (
            f"Command is on cooldown. Try again in {error.retry_after:.1f} seconds."
        )
    else:
        logger.exception("Unhandled application command exception: %s", error)
        message = "An unexpected internal error occurred while processing this command."

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


class CommunityBot(commands.Bot):
    """Custom Discord Bot client managing extensions and application commands."""

    def __init__(self, settings: Settings) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )
        self.settings = settings
        self.tree.error(handle_app_command_error)

    async def setup_hook(self) -> None:
        """Load configured cogs and conditionally synchronize application commands."""
        for extension in INITIAL_EXTENSIONS:
            await self.load_extension(extension)
            logger.info("Loaded extension: %s", extension)

        if self.settings.sync_commands_on_startup:
            logger.info("Synchronizing application command tree globally...")
            synced = await self.tree.sync()
            logger.info("Synchronized %d application command(s)", len(synced))
        else:
            logger.info(
                "Skipping startup command sync (SYNC_COMMANDS_ON_STARTUP=false). Use /sync to register."
            )

    async def on_ready(self) -> None:
        """Handle post-connection initialization and presence setup."""
        if not self.user:
            return

        logger.info("Logged in as %s (ID: %s)", self.user.name, self.user.id)
        invite_url = (
            f"https://discord.com/oauth2/authorize?client_id={self.user.id}"
            f"&permissions={self.settings.permissions}&scope=bot%20applications.commands"
        )
        logger.info("OAuth2 Invite URL: %s", invite_url)

        presence_text = self.settings.discord_invite_link.replace(
            "http://", ""
        ).replace("https://", "")
        await self.change_presence(activity=discord.Game(presence_text))
