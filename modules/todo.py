import textwrap

from discord.ext import commands


class Todo:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.is_owner()
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            result = '=============Todo List============='
            width = len(result)
            end = '\n' + '=' * width
            if self.bot.redis_db.exists('todo'):
                todolist = self.bot.redis_db.lrange('todo', 0, -1)
                for n, x in enumerate(todolist):
                    result += '\n' + '\n'.join(textwrap.wrap('{0}. {1}'.format(n+1, x.decode('utf-8')), width=width))
                result += end
                await ctx.send('```{}```'.format(result))
            else:
                result += end
                await ctx.send('```{}```'.format(result))

    @todo.command()
    async def add(self, ctx, *, msg: str):
        self.bot.redis_db.rpush('todo', msg)
        await ctx.message.add_reaction('✅')

    @todo.command()
    async def rm(self, ctx, index: int):
        index -= 1
        if self.bot.redis_db.exists('todo'):
            if 0 <= index < self.bot.redis_db.llen('todo'):
                value = self.bot.redis_db.lindex('todo', index)
                self.bot.redis_db.lrem('todo', 1, value)
                await ctx.message.add_reaction('✅')
                return

        await ctx.say('Invalid Number')

    @todo.command()
    async def edit(self, ctx, *, args):
        args = args.split(' ', 1)
        if not args[0].isnumeric():
            await ctx.send('Wrong syntax. {}todo edit [index] [value]')
            return
        index = int(args[0])
        value = args[1]
        index -= 1
        if self.bot.redis_db.exists('todo'):
            if 0 <= index < self.bot.redis_db.llen('todo'):
                self.bot.redis_db.lset('todo', index, value)
                await ctx.message.add_reaction('✅')


def setup(bot):
    bot.add_cog(Todo(bot))