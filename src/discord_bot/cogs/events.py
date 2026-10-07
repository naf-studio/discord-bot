"""Event listeners for member lifecycle and guild events."""

import logging

import discord
from discord.ext import commands

from discord_bot.config import Settings

logger = logging.getLogger(__name__)


class EventsCog(commands.Cog):
    """Cog handling guild lifecycle events, membership auditing, and boost tracking."""

    def __init__(self, bot: commands.Bot, settings: Settings) -> None:
        self.bot = bot
        self.settings = settings

    async def _send_audit_embed(
        self,
        channel_id: int,
        embed: discord.Embed,
    ) -> None:
        if channel_id <= 0:
            return

        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            logger.warning(
                "Audit channel %s is not accessible as a text channel", channel_id
            )
            return

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            logger.error("Missing permissions to send embed in channel %s", channel_id)
        except discord.HTTPException as exc:
            logger.error(
                "HTTP error dispatching audit embed to channel %s: %s",
                channel_id,
                exc,
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Audit member join events to designated channel."""
        embed = discord.Embed(
            description=f"{member.mention} has joined the server.",
            color=discord.Color.green(),
        )
        embed.add_field(name="Username", value=f"`{member.name}`", inline=True)
        embed.add_field(name="User ID", value=f"`{member.id}`", inline=True)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await self._send_audit_embed(self.settings.join_channel_id, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """Audit member departure events to designated channel."""
        embed = discord.Embed(
            description=f"{member.mention} has left the server.",
            color=discord.Color.red(),
        )
        embed.add_field(name="Username", value=f"`{member.name}`", inline=True)
        embed.add_field(name="User ID", value=f"`{member.id}`", inline=True)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await self._send_audit_embed(self.settings.leave_channel_id, embed)

    @commands.Cog.listener()
    async def on_guild_update(
        self, before: discord.Guild, after: discord.Guild
    ) -> None:
        """Detect and log guild boost level and count changes."""
        if not self.settings.boost_channel_id:
            return

        if after.premium_subscription_count > before.premium_subscription_count:
            embed = discord.Embed(
                title="Server Boost Received!",
                description=(
                    f"The server has reached **{after.premium_subscription_count}** boosts "
                    f"(Tier {after.premium_tier})."
                ),
                color=discord.Color.fuchsia(),
            )
            await self._send_audit_embed(self.settings.boost_channel_id, embed)


async def setup(bot: commands.Bot) -> None:
    """Register EventsCog with the bot instance."""
    settings = getattr(bot, "settings", Settings(bot_token="placeholder"))
    await bot.add_cog(EventsCog(bot, settings))
