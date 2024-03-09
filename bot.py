from twitchio.ext import commands
import os 
from dotenv import load_dotenv
import vt
load_dotenv()
client_auth=os.getenv('CLIENT_ID')
bot_auth_token=os.getenv('AUTH_TOKEN')
client = vt.Client(client_auth)
import nest_asyncio
nest_asyncio.apply()

def scan(user_url):
    retuned_values=[]
    url_id = vt.url_id(user_url)
    url = client.get_object("/urls/{}", url_id)
    return_var=url.last_analysis_stats
    print(return_var['malicious'])
    print(return_var['suspicious'])
    retuned_values.append(return_var['malicious'])
    retuned_values.append(return_var['suspicious'])
    return (retuned_values)

def closer():
    client.close()


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=bot_auth_token, prefix='?', initial_channels=['thefozzybear'])
    
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')
    @commands.command()
    async def scan_call(self, ctx: commands.Context,message):
        marks=scan(message)
        if marks[0]>2:
            await ctx.send(f'Hello {ctx.author.name}! the link you are sending is malcious')
        elif marks[1]>5:
            await ctx.send(f'Hello {ctx.author.name}! the link you are sending is Sussy')
        else:
            await ctx.send(f'Hello {ctx.author.name}! the link you are sending is clear')    
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.

