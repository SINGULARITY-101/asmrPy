import discord
from discord.ext import commands
from github import Github
import base64
from mdutils.mdutils import MdUtils
import json

repo = None
readmeFile = None
mdFile = None
categories = []
f = open('config.json')
tokens = json.load(f)

def convertFromB64(encoded):
    base64_bytes = encoded.encode("utf-8")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("utf-8")
    return string 

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    global repo, readmeFile, mdFile
    g = Github(tokens['github_token'])
    repo = g.get_repo("j23saw/asmr-test-lab")
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def addDomain(ctx, *, category):
    global repo, readmeFile, mdFile
    readmeFile = repo.get_contents("LOCAL_README.md")
    mdFile = MdUtils(file_name = "LOCAL_README.md")
    mdFile.new_header(level=1, title="Compilation Of DSC-RAIT resources")
    mdFile.new_paragraph("This is a ``README.md`` file generated by asmrPy to test it's capabilities. Stay tuned for more updates!")
    categories.append(category)
    for c in categories:
        mdFile.new_header(level = 2, title = c)
    mdFile.create_md_file()
    text = mdFile.read_md_file(file_name = "LOCAL_README.md")
    repo.update_file(readmeFile.path, "file update",  text, readmeFile.sha)
    print(text)
    await ctx.send(f'`{category}` domain added successfully!')
    return

@client.command()
async def domains(ctx):
    global repo
    contents = repo.get_contents("LOCAL_README.md")
    await ctx.send(f'```markdown{convertFromB64(contents.content)}```')

client.run(tokens['discord_token'])
