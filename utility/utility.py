import discord
from discord.ext import commands


class UtilityExamples(commands.Cog):
    """Semplici comandi di utilità (Plugin  tradotto da [Italian Riky](https://github.com(Italian-Riky))"""
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command()
    async def say(self, ctx, *, message: commands.clean_content):
        """Ripeto dopo di te"""
        await ctx.send(message)

    @commands.group(invoke_without_command=True)
    async def group(self, ctx):
        """Consente all'utente di impostare il proprio gruppo"""
        await ctx.send_help(ctx.command)

    @group.command(name='set')
    async def set_(self, ctx, group_name: str.title):
        """Imposta il loro gruppo"""
        valid_groups = ('Rosso', 'Verde', 'Blu')
        if group_name not in valid_groups:
            await ctx.send('Gruppo invalido. Scegline uno tra: ' + ', '.join(valid_groups))
        else:
            await self.db.find_one_and_update(
                {'user_id': str(ctx.author.id)},
                {'$set': {'group': group_name}},
                upsert=True
            )
            await ctx.send(f'Benvenuto in {group_name}!')

    @group.command()
    async def get(self, ctx, member: discord.Member = None):
        """Trova il gruppo di una persona."""
        member = member or ctx.author
        data = await self.db.find_one({'user_id': str(member.id)})
        if data:
            await ctx.send(f"{member.name} è in {data['group']}!")
        else:
            await ctx.send(f"{member.name} non ha scelto un gruppo :(")

    @commands.has_permissions(kick_members=True)
    @group.command()
    async def reset(self, ctx, member: discord.Member):
        """Reimposta il gruppo di una persona 
        Disponibile solo per i moderatori con il permesso kick_members """
        await self.db.find_one_and_delete({'user_id': str(member.id)})
        await ctx.send('Membro resettato')


def setup(bot):
    bot.add_cog(UtilityExamples(bot))
