import subprocess
from typing import Optional

from discord.ext import commands

import snakeboxed


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot, pm2_name: str):
        self.bot = bot
        self.pm2_name = pm2_name

    @commands.command(hidden=True, aliases=['u'])
    @commands.is_owner()
    async def update(self, ctx: commands.Context, commit_id: Optional[str]):
        """Update the bot."""
        await ctx.send(snakeboxed.__version__)

        pull_command = ['pm2', 'pull', self.pm2_name]
        if commit_id is not None:
            pull_command.append(commit_id)
        restart_command = ['pm2', 'restart', self.pm2_name]

        for command_list in pull_command, restart_command:
            command = ' '.join(command_list)
            await ctx.send(f'```bash\n{command}\n```')
            # capture all output in command result stdout together
            command_result_bytes = subprocess.run(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            command_result = command_result_bytes.stdout.decode(encoding='utf_8')
            await ctx.send(f'```\n{command_result}\n```')