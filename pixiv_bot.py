from distutils.log import error
from pydoc import describe
from urllib.parse import DefragResult
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import asyncio
import random
from os import system
import time
import os
from pixivpy3 import *
from pixiv_functions import *
from pixiv_search_leaderboard import leaderboard_main
from pixiv_user_research import user_main
from pixiv_search import search_main
from downloader import downloader
from dotenv import load_dotenv
from pixiv_search_id import *
from pixiv_related import *
import json
#imports


#Pixiv API oauth token setup
refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0" 
access = access_token_renewer(refresh)
api.set_auth(refresh_token=refresh,access_token=access)


#api & bot client setup
load_dotenv()
api = AppPixivAPI()
bot = commands.Bot(command_prefix='p!', description='A pixiv bot',help_command=None)



#environment vars
user_config_file = "user_settings.json"
global_r18switch = False

try:
    nightmare_path = os.getenv("NIGHTMARE_PATH")
    TOKEN = os.getenv("DISCORD_TOKEN")
    #Discord bot token

except:
    nightmare_path = os.environ.get("NIGHTMARE_PATH")
    TOKEN = os.environ.get("DISCORD_TOKEN")
    #Discord bot token


# True for allow r18 False for no allow r18

like_limit_cap = 100
#############################################################################

#open bot message

@bot.event
async def on_ready():  
    print(discord.__version__) 
    activity_w = discord.Activity(type=discord.ActivityType.playing, name="和作者大人色色...❤️")

    await bot.change_presence(status=discord.Status.dnd, activity=activity_w)

@bot.command()
async def register(ctx):
    """
    Add a new user to user settings file
    """

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    for user_id in user_settings:
        if user_id["user"] == ctx.message.author.id:
            await ctx.send("Already registered.")
            return

    #var for user settings
    uid = ctx.message.author.id
    personal_detail = None
    r18allow = False
    pic_amount = 3
    p_details = False
    favorite = []
    like_limit = 3000

    user_settings.append({"user" : uid, "personal_detail" : personal_detail, "r18allow" : r18allow, "picture_amount" : pic_amount, "print_details" : p_details, "favorite" : favorite, "like_limit" : like_limit})

    print(user_settings)
    with open(user_config_file, "w") as fhandle:
        json.dump(user_settings, fhandle, indent=4)

    await ctx.send("Registered. Please use **p!settings** to customize your settings!")

@bot.command()
async def relog(ctx):
    """
    p!relog 

    relogging access token (NOT WORKING)
    """

    relog_text = await ctx.send(embed=discord.Embed(title="Relogging access token..."))
    global access
    global refresh
    try: #success relogging
        access = access_token_renewer(refresh)
        api.set_auth(refresh_token=refresh,access_token=access)

        await relog_text.delete()
        msg = await ctx.send(embed=discord.Embed(title="Success relogged"))
        await asyncio.sleep(2)
        await msg.delete()

        return api, access

    except: #failed relogging
        
        await relog_text.delete()
        msg = await ctx.send(embed=discord.Embed(title="Relog failed."))
        await asyncio.sleep(2)
        await msg.delete()

        return

@bot.command(aliases=["setting","s","set"])
async def settings(ctx, *arg):
    """
    settings command to interact with user_settings file

    p!settings [keyword] [value]
    """

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if not user_registered(user_settings, ctx.message.author.id):
        await ctx.send("Haven't registered? Please register yourself with command: p!register.")
        return

    if len(arg) == 0:
        '''
        when theres no arguments send author's settings value 
        '''

        for users in user_settings:

            if users["user"] == ctx.message.author.id:

                message = discord.Embed(title=f"{ctx.author} 's settings:",color=0xaaaaaa)
                message.add_field(name = 'Informations:', value= str(users["personal_detail"]), inline = False)
                message.add_field(name = 'R18:', value = str(users["r18allow"]), inline = True)
                message.add_field(name = 'Print picture details:', value = str(users["print_details"]), inline = False)

                message.add_field(name = 'Search like limit:', value = str(users["like_limit"]), inline = True)
                message.add_field(name = 'Amount of picture wanted:', value = str(users["picture_amount"]), inline = True)
                

                message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")
                
                file=[discord.File("Karl_hsiao.png")]

                await ctx.send(embed=message, files=file)

                return

        await ctx.send("Haven't registered? Please register yourself with command: **p!register**.")
        return

    elif arg[0] == "informations" or arg[0] == "personal detail" or arg[0] == "i" or arg[0] == "info":
        '''
        setting for information (anything user want to say)
        '''

        if len(arg) == 2:

            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    users["personal_detail"] = arg[1]
                    if len(arg[1]) < 50:
                        msg = discord.Embed(title="Set your **Informations** to \"**" + str(arg[1]) + "**\".",color=0xaaaaaa)
                        
                    
                    else:
                        await ctx.send("Too many charactors!")
                        return
            

        else:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    msg = discord.Embed(title="Your current **information** is \"**" + str(users["personal_detail"]) + "**\".",color=0xaaaaaa)

    elif arg[0] == "r18allow" or arg[0] == "r" or arg[0] == "18" or arg[0] == "r18":
        """
        Set that if user want r18 or not
        """
        if len(arg) == 2:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    if arg[1] == "true" or arg[1] == "t" or arg[1] == "1" or arg[1] == "allow" or arg[1] == "open" or arg[1] == "a" or arg[1] == "enable":
                        users["r18allow"] = True
                        msg = discord.Embed(title="Set your **R18** to **True**.",color=0xaaaaaa)
                  
                    
                    elif arg[1] == "false" or arg[1] == "f" or arg[1] == "0" or arg[1] == "disallow" or arg[1] == "close" or arg[1] == "d" or arg[1] == "disable":
                        users["r18allow"] = False
                        msg = discord.Embed(title="Set your **R18** to **False**",color=0xaaaaaa)
              
                    
                    else:
                        await ctx.send("Invaild input!")
                        return


        else:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    msg = discord.Embed(title="Your current **R18** setting is **" + str(users["r18allow"]) + "**.",color=0xaaaaaa)

    elif arg[0] == "picture wanted" or arg[0] == "pw" or arg[0] == "p" or arg[0] == "picture" or arg[0] == "amount" or arg[0] == "pa" or arg[0] == "paw" or arg[0] == "pic" or arg[0] == "pictures":
        """
        set how many pic user want in one result
        """
        if len(arg) == 2:
            
            for users in user_settings:
                if users["user"] == ctx.message.author.id:

                    try:
                        if int(arg[1]) > 10:
                            await ctx.send("Too much, please set it under 10.")
                            return

                        users["picture_amount"] = int(arg[1])
                        msg = discord.Embed(title="Set your **picture_amount** to **" + str(arg[1]) + "**.",color=0xaaaaaa)


                    except:
                        await ctx.send("Invaild input!")
                        return
  
        else:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    msg = discord.Embed(title="Your current **picture amount** is **" + str(users["picture_amount"]) + "**.",color=0xaaaaaa)

    elif arg[0] == "d" or arg[0] == "picture detail" or arg[0] == "print detail" or arg[0] == "print picture detail" or arg[0] == "ppd" or arg[0] == "pd" or arg[0] == "details" or arg[0] == "detail":
        """
        set if user want details in results
        (detail contents bookmarks and tags that picture have)

        """
        if len(arg) == 2:

            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    if arg[1] == "true" or arg[1] == "t" or arg[1] == "1" or arg[1] == "allow" or arg[1] == "open" or arg[1] == "a" or arg[1] == "enable":
                        users["print_details"] = True
                        msg = discord.Embed(title="Set your Detail printer to **True**.",color=0xaaaaaa) 
                   
                    
                    elif arg[1] == "false" or arg[1] == "f" or arg[1] == "0" or arg[1] == "disallow" or arg[1] == "close" or arg[1] == "d" or arg[1] == "disable":
                        users["print_details"] = False
                        msg = discord.Embed(title="Set your **Detail_printer** to **False**",color=0xaaaaaa)
           

                    else:
                        await ctx.send("Invaild input!")
                        return
        else:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    msg = discord.Embed(title="Your current **print picture detail** is **" + str(users["print_details"]) + "**.",color=0xaaaaaa)

    elif arg[0] == "like" or arg[0] == "ll" or arg[0] == "Like" or arg[0] == "l" or arg[0] == "L" or arg[0] == "limit" or arg[0] == "like_limit":
        if len(arg) == 2:

            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        if int(arg[1]) > 10000:
                            await ctx.send("Over limit!")
                            return
                        
                        users["like_limit"] = int(arg[1])
                        msg = discord.Embed(title="Set your **Like limit** to **" + str(arg[1]) + "**.",color=0xaaaaaa)
       
                    except:
                        await ctx.send("Invaild input!")
                
        else:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    msg = discord.Embed(title="Your current **like limit** is **" + str(users["like_limit"]) + "**.",color=0xaaaaaa)

    else:
        await ctx.send("Invaild input!")
        return


    with open(user_config_file, "w") as fhandle:
        json.dump(user_settings, fhandle, indent=4)

    await ctx.send(embed=msg)
    return

@bot.command()
async def ping(ctx):
    """
    Pong!
    """
    await ctx.send("Pong!")

@bot.command(pass_context=True)
async def test(ctx):
    """
    Send a easteregg text (❤️Nightmare❤️ sama pic)
    """

    number = str(random.randint(1,15))
    number = number.zfill(4)

    nightmare = "Nightmare_" + number + ".jpg"

    messages = discord.Embed(title="Nothing to see here.",description="But she's my wife tho c:",color=0xeeeecc)
    
    files=[
        discord.File(nightmare_path + nightmare, filename=nightmare), 
        discord.File("Karl_hsiao.png"),
        ]

    messages.set_image(url=f"attachment://{nightmare}")
    messages.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")
    await ctx.send(embed=messages, files=files)

@bot.command(pass_context=True, aliases=["r18","18"])
async def nsfw(ctx):
    """
    allow or disallow r18 in general
    """
    global global_r18switch
    if global_r18switch == False:
        global_r18switch = True
        await ctx.send("Enabled r18.")

    else:
        global_r18switch = False
        await ctx.send("Disabled r18.")
        
@bot.command()
async def credit(ctx):
    """
    send credit message
    """

    await ctx.channel.send("``` Bot by Karl_hsiao\nThanks for all people that helped me!\n* *Special thanks* *```")

@bot.command()
async def easteregg(ctx):
    """
    send easter egg message
    """

    await ctx.channel.send("Oh Damn! You found this easter egg! Shh don't tell anyone yet!")

@bot.command(pass_context=True, aliases=["help","helps","command","commands"])
async def h(ctx):
    """
    send help/commands message
    """

    msg = discord.Embed(title="香圖bot 指令集", color=0xcc88dd, description="()是必須要填的內容，[]是不一定要填的內容")
    msg.add_field(name="註冊帳號",value="p!register",inline=False)
    msg.add_field(name="找圖指令",value="p!search (關鍵字)\np!user (pixiv user id)\np!leaderboard [關鍵字]\np!image (pixiv illust id)\np!recommended [tag其他人]",inline=True)
    msg.add_field(name="使用者設定",value="**p!settings [setting] [value]**\np!settings info (任何東西)\np!settings amount (多少圖)\np!settings r18 (true或false)\np!settings pic (你一次要出現多少圖)\np!settings detail (true或false)\np!settings like_limit (like數下限)",inline=True)
    msg.add_field(name="喜好設定",value="p!favorite [add/remove/add_user/list/@user] [pixiv_illust_id]",inline=False)

    await ctx.channel.send(embed=msg)

@bot.command()
async def favorite(ctx, *arg):
    '''
    
    Favorite system:


    '''
    
    add_favorites = []

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if not user_registered(user_settings, ctx.message.author.id):
        await ctx.send("Haven't registered? Please register yourself with command: p!register.")
        return

    if len(arg) == 0:
        favorites = ""
        loading_picture = "good_pic"

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        r18switch = r18allow and global_r18switch
        
        rng = random.randint(0, len(favorite) - 1)

        loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

        search_results = search_id_main(favorite[rng])

        await loading_screen.delete()

        if search_results != None and search_results != []:

            await ctx.send(str(len(search_results)) + " result(s) found.")

            for search_result in search_results:


                title = search_result[0]
                pic_url = search_result[1]
                bookmarks = search_result[2]
                original_tags = search_result[3]
                id = search_result[4]
            
                downloader(pic_url, loading_picture)
                               
                message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
                fileplace = "attachment://" + loading_picture + ".jpg"
                message.set_image(url=fileplace)
                message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                msg = await ctx.send(embed=message, files=files)
                await msg.add_reaction("❤️")


                if os.path.exists(loading_picture + ".jpg"):
                    os.remove(loading_picture + ".jpg")
    
            return

        else:
            await ctx.send(embed=discord.Embed(title="No result found."))

    elif arg[0] == "add":
        if len(arg) >= 2:

            fav_args = arg[1:]
            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        
                        for ids in fav_args:
                            if is_id_valid(ids):
                                users["favorite"].append(int(ids))
                                add_favorites.append(int(ids))

                            else:
                                await ctx.send("Picture id not valid!")
                                return

                        msg = discord.Embed(title="Success added " + str(add_favorites) + " to your favorites.")
                     
                    except:
                        await ctx.send("Invaild input!")

        else:
            await ctx.send("Missing arguments!")
            return

    elif arg[0] == "remove":
        if len(arg) >= 2:

            fav_args = arg[1:]
            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        if len(fav_args) == 0:
                            await ctx.send("Missing arguments!")
                            return

                        for ids in fav_args:

                            try:
                                users["favorite"].remove(int(ids))
                            except:
                                await ctx.send("You don't have " + str(ids) + " in your favorites!")
                                return

                            add_favorites.append(int(ids))

                        msg = discord.Embed(title="Success removed " + str(add_favorites) + " in your favorites.")
                        
                    except:
                        await ctx.send("Invaild input!")
            

        else:
            await ctx.send("Missing arguments!") 
            return

    elif arg[0] == "list":
        favorites = ""

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        for i in favorite:
            #favorites = favorites + "[" + str(i) + "](" + "https://www.pixiv.net/artworks/" + str(i) + ">" + ")\n"
            favorites = favorites + str(i) + "\n"

        msg = discord.Embed(title=f"{ctx.author.mention}'s Favorite: \n",description=favorites)
    
    elif arg[0] == "add_user":
        if len(arg) >= 2:
            
            adding_ids = []
            user_id = arg[1:]
            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

                        results = user_main(user_id, need=100, r18allow=r18allow)

                        for result in results:
                            adding_ids.append(result[4])

                        for ids in adding_ids:
                            if is_id_valid(ids) and (ids not in users["favorite"]):
                                users["favorite"].append(int(ids))

                        msg = discord.Embed(title="Success added " + str(user_id) + "'s marked to your favorites.")

                    except:
                        await ctx.send("Invaild input!")

        else:
            await ctx.send("Missing arguments!")
            return
    
    else:
        try:

            favorites = ""
            tag_user = arg[0]
            user_id = tag_user[3:-1]

            personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(int(user_id))

            for i in favorite:
                favorites = favorites + str(i) + "\n"

            await ctx.send(f">>> {tag_user}'s Favorite: \n" + favorites)
            return

        except:
            await ctx.send("Invalid argument or Invalid user!")
            return

    with open(user_config_file, "w") as fhandle:
        json.dump(user_settings, fhandle, indent=4)

    await ctx.send(embed=msg)
    return

@bot.command(aliases=["recommend", "re", "r"])
async def recommended(ctx, *arg):

    loading_picture = "good_pic"

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if len(arg) == 0:

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        if len(favorite) == 0:
            await ctx.reply("You haven't set anything to your favorites yet! try using **p!favorite [PixivID]** \n or click the heart below other illustrations to add favorites")
            return

        r18switch = r18allow and global_r18switch

        rng = random.randint(0, len(favorite) - 1)

        loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

        search_results = main_related(favorite[rng], pic_amount, r18switch)

        await loading_screen.delete()

        if search_results != None and search_results != []:

            await ctx.send(str(len(search_results)) + " result(s) found.")

            for search_result in search_results:

                title = search_result[0]
                pic_url = search_result[1]
                bookmarks = search_result[2]
                original_tags = search_result[3]
                id = search_result[4]
            
                downloader(pic_url, loading_picture)
                               
                message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
                fileplace = "attachment://" + loading_picture + ".jpg"
                message.set_image(url=fileplace)
                message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                msg = await ctx.send(embed=message, files=files)
                await msg.add_reaction("❤️")


                if os.path.exists(loading_picture + ".jpg"):
                    os.remove(loading_picture + ".jpg")
    
            return

        else:
            await ctx.send(embed=discord.Embed(title="No result found."))

    elif len(arg) == 1:
        try:
            tag = arg[0]
            user_id = int(tag[3:-1])

            if (not is_number(user_id)):
                await ctx.channel.send("Invalid argument!")
                return

        except:
            await ctx.channel.send("Invalid argument!")
            return


        for users in user_settings:

            if user_id == users["user"]:

                unuse_personal_detail, unuse_r18allow, unuse_pic_amount, unuse_p_details, favorite, unuse_like_limit = find_user_settings(user_id)

                personal_detail, r18allow, pic_amount, p_details, unuse_favorite, like_limit = find_user_settings(ctx.message.author.id)
                
                r18switch = r18allow and global_r18switch

                rng = random.randint(0, len(favorite) - 1)

                loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

                search_results = main_related(favorite[rng], pic_amount, r18switch)

                await loading_screen.delete()

                if search_results != None and search_results != []:


                    for search_result in search_results:


                        title = search_result[0]
                        pic_url = search_result[1]
                        bookmarks = search_result[2]
                        original_tags = search_result[3]
                        id = search_result[4]
            
                        downloader(pic_url, loading_picture)
                               
                        message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
                        fileplace = "attachment://" + loading_picture + ".jpg"
                        message.set_image(url=fileplace)
                        message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                        if p_details == True:
                            message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                            message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                        files=[                    
                            discord.File(loading_picture + ".jpg")
                            ,discord.File("Karl_hsiao.png")
                            ]

                        msg = await ctx.send(embed=message, files=files)
                        await msg.add_reaction("❤️")

                        if os.path.exists(loading_picture + ".jpg"):
                            os.remove(loading_picture + ".jpg")
    
                    return

                else:
                    await ctx.send(embed=discord.Embed(title="No result found."))

        await ctx.send("The user is not registered yet! Try use p!register to register.")
        return
    
    else:
        await ctx.channel.send("Invalid argument!")
        return
        
@bot.command()
async def leaderboard(ctx, *arg):
    loading_picture = "good_pic"
    personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)
    
    try:
        search = arg[0]
    except:
        search = ""

    try:
        needs = int(arg[1])
    except:
        needs = pic_amount

    r18switch = (global_r18switch and r18allow)

    loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc))
    
    search_results = leaderboard_main(search, needs, r18switch)

    await loading_screen.delete()

    if search_results != None and search_results != []:

        await ctx.send(str(len(search_results)) + " result(s) found.")

        for search_result in search_results:


            title = search_result[0]
            pic_url = search_result[1]
            bookmarks = search_result[2]
            original_tags = search_result[3]
            id = search_result[4]
            
            downloader(pic_url, loading_picture)
                               
            message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
            fileplace = "attachment://" + loading_picture + ".jpg"
            message.set_image(url=fileplace)
            message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            msg = await ctx.send(embed=message, files=files)
            await msg.add_reaction("❤️")


            if os.path.exists(loading_picture + ".jpg"):
                os.remove(loading_picture + ".jpg")
    
        return

    else:
        await ctx.send(embed=discord.Embed(title="No result found."))

@bot.command()
async def user(ctx, *arg):

    personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

    try:
        user_id = arg[0]

    except:
        await ctx.channel.send("Please enter a user id.")
        return

    if not is_number(user_id):
        await ctx.channel.send("Invalid user id!")
        return

    amount = pic_amount
    search = ""
    loading_picture = "good_pic"
    r18switch = (global_r18switch and r18allow)

    try:
        arg_1 = arg[1]
        if arg_1[0:1] == "n/":
            search = arg_1[2:]
        elif is_number(arg_1):
            amount = arg[1]
            search = ""
        else:
            search = arg[1]

    except:
        pass    

    try:
        amount = arg[2]
    except:
        pass
    
    loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc))

    search_results = user_main(user_id, search, int(amount), r18switch)

    await loading_screen.delete()

    if search_results != None and search_results != []:
            
            await ctx.send(str(len(search_results)) + " result(s) found.")

            for search_result in search_results:


                title = search_result[0]
                pic_url = search_result[1]
                bookmarks = search_result[2]
                original_tags = search_result[3]
                id = search_result[4]
            
                downloader(pic_url, loading_picture)
                               
                message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
                fileplace = "attachment://" + loading_picture + ".jpg"
                message.set_image(url=fileplace)
                message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                msg = await ctx.send(embed=message, files=files)
                await msg.add_reaction("❤️")


                if os.path.exists(loading_picture + ".jpg"):
                    os.remove(loading_picture + ".jpg")
    
            return

    else:
        await ctx.send(embed=discord.Embed(title="No result found."))
        
@bot.command()
async def search(ctx, *arg):

    personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)
    
    try:
        search = arg[0]

    except:
        await ctx.channel.send("Please enter a word you wanted to search for.")
        return

    amount = pic_amount
    loading_picture = "good_pic"
    r18switch = (global_r18switch and r18allow)

    loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc))    

    search_results = search_main(search, amount, like_limit, r18switch)
    
    await loading_screen.delete()

    
    if search_results != None and search_results != []:

        await ctx.send(str(len(search_results)) + " result(s) found.")

        for search_result in search_results:


            title = search_result[0]
            pic_url = search_result[1]
            bookmarks = search_result[2]
            original_tags = search_result[3]
            id = search_result[4]
            
            downloader(pic_url, loading_picture)
                               
            message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
            fileplace = "attachment://" + loading_picture + ".jpg"
            message.set_image(url=fileplace)
            message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            msg = await ctx.send(embed=message, files=files)
            await msg.add_reaction("❤️")


            if os.path.exists(loading_picture + ".jpg"):
                os.remove(loading_picture + ".jpg")
    
        return

    else:
        await ctx.send(embed=discord.Embed(title="No result found."))

@bot.command()
async def image(ctx, *arg):
    
    personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

    try:
        search = arg[0]

    except:
        await ctx.channel.send("Please enter a Pixiv image id you wanted to search for.")
        return

    r18switch = (global_r18switch and r18allow)
    loading_picture = "good_pic"

    loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc))    

    search_results = search_id_main(search)

    await loading_screen.delete()

    if search_results != None and search_results != []:

        await ctx.send(str(len(search_results)) + " result(s) found.")

        for search_result in search_results:


            title = search_result[0]
            pic_url = search_result[1]
            bookmarks = search_result[2]
            original_tags = search_result[3]
            id = search_result[4]
            
            downloader(pic_url, loading_picture)
                               
            message = discord.Embed(title=f"{title}",description=f"original link: <https://www.pixiv.net/artworks/{id}>",color=0xd4f1f9)
            fileplace = "attachment://" + loading_picture + ".jpg"
            message.set_image(url=fileplace)
            message.set_footer(text="By Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            msg = await ctx.send(embed=message, files=files)
            await msg.add_reaction("❤️")


            if os.path.exists(loading_picture + ".jpg"):
                os.remove(loading_picture + ".jpg")
    
        return

    else:
        await ctx.send(embed=discord.Embed(title="No result found."))

@bot.command(pass_context=True)
async def testing(ctx, *arg):
    #n = arg[0]
    #await ctx.send(n[3:-1])

    favorites = ""

    personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

    for i in favorite:
        favorites = favorites + "[" + str(i) + "](" + "https://www.pixiv.net/artworks/" + str(i) + ">" + ")\n"
        if i == 85348588:
            break

    msg = discord.Embed(title=f"{ctx.author.mention}'s Favorite: \n",description=favorites)

    await ctx.channel.send(embed=msg)
    return

@bot.command(pass_context=True)
async def suggestion(ctx, arg):


    pass

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    raw_msg = await channel.fetch_message(payload.message_id)
    user = payload.user_id

    if user == 839523310777925703:
        return

    embeds = raw_msg.embeds
    emoji = str(payload.emoji)

    for embed in embeds:
        msg = embed.to_dict()
    
    try:
        with open(user_config_file, "r") as fhandle:
            user_settings = json.load(fhandle)

        if emoji == "❤️":
            try:
                pic_id = msg["description"]
                pic_id = pic_id[-9:-1]
                for users in user_settings:
                    if users["user"] == user:
                        if int(pic_id) in users["favorite"]:
                            msg = discord.Embed(title="This ID is already added to your favorite.")
                            await raw_msg.reply(embed=msg, mention_author=False)
                            return

                        if is_id_valid(pic_id):
                            users["favorite"].append(int(pic_id))

                        else:
                            await channel.send("Picture id not valid!")
                            return

                        for image in search_id_main(pic_id):
                            pic_name = image[0]

                        user_name = await bot.fetch_user(user)

                        msg = discord.Embed(title="Success added \"" + str(pic_name) + "\" to " + str(user_name) + " favorites.")
                    
                        await raw_msg.reply(embed=msg, mention_author=False)
                        
                        with open(user_config_file, "w") as fhandle:
                            json.dump(user_settings, fhandle, indent=4)
                            return
            except:
                return

            await raw_msg.reply("Haven't registered? Please register yourself with command: p!register.")
            return
        
    except:
        await raw_msg.reply("Some error has occurred, please report this bug to the bot author:\"Karl_hsiao#9522\"")
        return

@bot.event
async def on_raw_reaction_remove(payload):

    channel = bot.get_channel(payload.channel_id)
    raw_msg = await channel.fetch_message(payload.message_id)
    user = payload.user_id
    embeds = raw_msg.embeds
    emoji = str(payload.emoji)

    for embed in embeds:
        msg = embed.to_dict()
    
    try:
        with open(user_config_file, "r") as fhandle:
            user_settings = json.load(fhandle)

        if emoji == "❤️":
            try:
                pic_id = msg["description"]
                pic_id = pic_id[-9:-1]
                for users in user_settings:
                    if users["user"] == user:
                        
                        if is_id_valid(pic_id):
                            users["favorite"].remove(int(pic_id))

                        else:
                            await channel.send("Picture id not valid!")
                            return

                        for image in search_id_main(pic_id):
                            pic_name = image[0]

                        user_name = await bot.fetch_user(user)

                        msg = discord.Embed(title="Success removed \"" + str(pic_name) + "\" from " + str(user_name) + " favorites.")
                    
                        await raw_msg.reply(embed=msg, mention_author=False)
                        
                        with open(user_config_file, "w") as fhandle:
                            json.dump(user_settings, fhandle, indent=4)
                            return
                            
            except:
                return

            await raw_msg.reply("Haven't registered? Please register yourself with command: p!register.")
            return                        

    except:
        await raw_msg.reply("Some error has occurred, please report this bug to the bot author:\"Karl_hsiao#9522\"")
        return

bot.run(TOKEN)  
