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
from pixiv_search_id import *
from pixiv_related import *
import json


api = AppPixivAPI()

print(discord.__version__)

TOKEN = "DISCORD_TOKEN"

refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
access = access_token_renewer(refresh)


api.set_auth(refresh_token=refresh,access_token=access)

bot = commands.Bot(command_prefix='p!', description='A pixiv bot')

user_config_file = "user_settings.json"

global_r18switch = False
# True for allow r18 False for no allow r18

@bot.command()
async def register(ctx):
    registered = 0
    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    for user_id in user_settings:
        try:
            if user_id["user"] == ctx.message.author.id:
                await ctx.send("Already registered.")
                return
        except:
            pass

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
    relog_text = await ctx.send(embed=discord.Embed(title="Relogging access token..."))
    global access
    global refresh
    try:
        access = access_token_renewer(refresh)
        api.set_auth(refresh_token=refresh,access_token=access)

        await relog_text.delete()
        msg = await ctx.send(embed=discord.Embed(title="Success relogged"))
        await asyncio.sleep(2)
        await msg.delete()

        return

    except:
        
        await relog_text.delete()
        msg = await ctx.send(embed=discord.Embed(title="Relog failed."))
        time.sleep(2)
        await msg.delete()

        return

@bot.command()
async def settings(ctx, *arg):
    reg = False

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if len(arg) == 0:
        print("1")

        for users in user_settings:

            if users["user"] == ctx.message.author.id:

                message = discord.Embed(title=f"{ctx.author} 's settings:",color=0xaaaaaa)
                message.add_field(name = 'Informations:', value= str(users["personal_detail"]), inline = False)
                message.add_field(name = "R18:", value = str(users["r18allow"]), inline = True)
                message.add_field(name = 'Print picture details:', value = str(users["print_details"]), inline = False)

                message.add_field(name = 'Search like limit:', value = str(users["like_limit"]), inline = True)
                message.add_field(name = 'Amount of picture wanted:', value = str(users["picture_amount"]), inline = True)
                

                message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")
                
                file=[discord.File("Karl_hsiao.png")]

                await ctx.send(embed=message, files=file)
                #await ctx.send(f">>> {ctx.author.mention}'s settings:\n\n" + "Informations: **" + str(users["personal_detail"]) + "**\nR18: **" + str(users["r18allow"]) + "**\nAmount of picture wanted: **" + str(users["picture_amount"]) + "**\nSearch like limit: **" + str(users["like_limit"]) + "**\nPrint picture details: **" + str(users["print_details"]) + "**")


                return

        await ctx.send("Haven't registered? Please register yourself with command: **p!register**.")
        return

    elif arg[0] == "informations" or arg[0] == "personal detail" or arg[0] == "i" or arg[0] == "info":

        if len(arg) == 2:

            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    users["personal_detail"] = arg[1]
                    if len(arg[1]) < 50:
                        msg = discord.Embed(title="Setted your **Informations** to **" + str(arg[1]) + "**.")
                        reg = True
                    
                    else:
                        await ctx.send("Too many charactors!")
                        return
            

        else:
            await ctx.send("Invaild input!")
            return

    elif arg[0] == "r18allow" or arg[0] == "r" or arg[0] == "18" or arg[0] == "r18":

        if len(arg) == 2:
            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    if arg[1] == "true" or arg[1] == "t" or arg[1] == "1" or arg[1] == "allow" or arg[1] == "open" or arg[1] == "a" or arg[1] == "enable":
                        users["r18allow"] = True
                        msg = discord.Embed(title="Setted your **R18** to **True**.")
                        reg = True
                    
                    elif arg[1] == "false" or arg[1] == "f" or arg[1] == "0" or arg[1] == "disallow" or arg[1] == "close" or arg[1] == "d" or arg[1] == "disable":
                        users["r18allow"] = False
                        msg = discord.Embed(title="Setted your **R18** to **False**")
                        reg = True
                    
                    else:
                        await ctx.send("Invaild input!")
                        return


        else:
            await ctx.send("Invaild input!")
            return

    elif arg[0] == "picture wanted" or arg[0] == "pw" or arg[0] == "p" or arg[0] == "picture" or arg[0] == "amount" or arg[0] == "pa" or arg[0] == "paw" or arg[0] == "pic" or arg[0] == "pictures":

        if len(arg) == 2:
            
            for users in user_settings:
                if users["user"] == ctx.message.author.id:

                    try:
                        if int(arg[1]) > 10:
                            await ctx.send("Too much, please set it under 10.")
                            return

                        users["picture_amount"] = int(arg[1])
                        msg = discord.Embed(title="Setted your **picture_amount** to **" + str(arg[1]) + "**.")
                        reg = True

                    except:
                        await ctx.send("Invaild input!")
                        return
  
        else:
            await ctx.send("Invaild input!")
            return

    elif arg[0] == "d" or arg[0] == "picture detail" or arg[0] == "print detail" or arg[0] == "print picture detail" or arg[0] == "ppd" or arg[0] == "pd" or arg[0] == "details" or arg[0] == "detail":
        
        if len(arg) == 2:

            for users in user_settings:
                if users["user"] == ctx.message.author.id:
                    if arg[1] == "true" or arg[1] == "t" or arg[1] == "1" or arg[1] == "allow" or arg[1] == "open" or arg[1] == "a" or arg[1] == "enable":
                        users["print_details"] = True
                        msg = discord.Embed(title="Setted your Detail printer to **True**.") 
                        reg = True
                    
                    elif arg[1] == "false" or arg[1] == "f" or arg[1] == "0" or arg[1] == "disallow" or arg[1] == "close" or arg[1] == "d" or arg[1] == "disable":
                        users["print_details"] = False
                        msg = "Setted your **Detail_printer** to **False**"
                        reg = True

                    else:
                        await ctx.send("Invaild input!")
                        return

    elif arg[0] == "like" or arg[0] == "ll" or arg[0] == "Like" or arg[0] == "l" or arg[0] == "L" or arg[0] == "limit":
        if len(arg) == 2:

            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        if int(arg[1]) > 10000:
                            await ctx.send("Over limit!")
                            return
                        
                        users["like_limit"] = int(arg[1])
                        print("yes")
                        msg = "Setted your **Like limit** to **" + str(arg[1]) + "**."
                        reg = True
                    except:
                        await ctx.send("Invaild input!")
                

        else:
            await ctx.send("Invaild input!")
            return

    else:
        await ctx.send("Invaild input!")
        return

    if reg == True:

        with open(user_config_file, "w") as fhandle:
            json.dump(user_settings, fhandle, indent=4)

        await ctx.send(embed=msg)
        return

    else:
        await ctx.send(embed=discord.Embed(title="Haven't registered? Please register yourself with command: p!register."))
        return

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(pass_context=True)
async def test(ctx):
    messages = discord.Embed(title="Nothing to see here.",description="She's my wife tho c:",color=0xeeeecc)
    file=[
        discord.File("Nightmare.png"), 
        discord.File("Karl_hsiao.png"),
        ]

    messages.set_image(url="attachment://Nightmare.png")
    messages.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")
    await ctx.send(embed=messages, files=file)
    
    #await ctx.send("Nothing to see, but shes wife c:",file=discord.File("Nightmare.png"))

@bot.command(pass_context=True)
async def nsfw(ctx):
    global global_r18switch
    if global_r18switch == False:
        global_r18switch = True
        await ctx.send("Enabled r18.")

    else:
        global_r18switch = False
        await ctx.send("Disabled r18.")
        
@bot.command()
async def credit(ctx):
    await ctx.channel.send("``` Bot by Karl_hsiao\nThanks for all people that helped me!\n* *Special thanks* *```")

@bot.command()
async def easteregg(ctx):
    await ctx.channel.send("Oh Damn! You found this easter egg! Shh don't tell anyone yet!")

@bot.command()
async def h(ctx):
    await ctx.channel.send("helps")

@bot.command()
async def favorite(ctx, *arg):
    
    add_favorites = []
    reg = None

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if len(arg) == 0:
        favorites = ""
        fav_list = []
        loading_picture = "good_pic"

        

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        r18switch = r18allow and global_r18switch
        
        rng = random.randint(0, len(favorite) - 1)

        loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

        search_results = search_id_main(favorite[rng])

        await loading_screen.delete()

        if search_results != None and search_results != []:
            found = True

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
                message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                await ctx.send(embed=message, files=files)


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
                        reg = True
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
                        reg = True
                    except:
                        await ctx.send("Invaild input!")
            

        else:
            await ctx.send("Missing arguments!") 
            return

    elif arg[0] == "list":
        favorites = ""

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        for i in favorite:
            favorites = favorites + str(i) + "\n"
    
        reg = True
        msg = discord.Embed(title=f"{ctx.author.mention}'s Favorite: \n",description=favorites)
        

    
    elif arg[0] == "add_user":
        if len(arg) >= 2:
            
            adding_ids = []
            user_id = arg[1:]
            for users in user_settings:
                
                if users["user"] == ctx.message.author.id:

                    try:
                        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

                        results = user_main(user_id, need=30, r18allow=r18allow)

                        for result in results:
                            adding_ids.append(result[4])

                        for ids in adding_ids:
                            if is_id_valid(ids):
                                users["favorite"].append(int(ids))

                        msg = discord.Embed(title="Success added " + str(user_id) + "'s marked to your favorites.")
                        reg = True
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

    if reg == True:

        with open(user_config_file, "w") as fhandle:
            json.dump(user_settings, fhandle, indent=4)

        await ctx.send(embed=msg)
        return

    else:
        await ctx.send("Haven't registered? Please register yourself with command: p!register.")
        return

@bot.command()
async def recommended(ctx, *arg):

    add_favorites = []
    n = 0
    found = False
    loading_picture = "good_pic"

    with open(user_config_file, "r") as fhandle:
        user_settings = json.load(fhandle)

    if len(arg) == 0:

        personal_detail, r18allow, pic_amount, p_details, favorite, like_limit = find_user_settings(ctx.message.author.id)

        r18switch = r18allow and global_r18switch

        rng = random.randint(0, len(favorite) - 1)

        loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

        search_results = main_related(favorite[rng], pic_amount, r18switch)

        await loading_screen.delete()

        if search_results != None and search_results != []:
            found = True

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
                message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                await ctx.send(embed=message, files=files)


                if os.path.exists(loading_picture + ".jpg"):
                    os.remove(loading_picture + ".jpg")
    
            return

        else:
            await ctx.send(embed=discord.Embed(title="No result found."))

    elif len(arg) == 1:

        tag = arg[0]
        user_id = int(tag[3:-1])

        for users in user_settings:

            print(user_id, users["user"])

            if user_id == users["user"]:

                found = True

                unuse_personal_detail, unuse_r18allow, unuse_pic_amount, unuse_p_details, favorite, unuse_like_limit = find_user_settings(user_id)

                personal_detail, r18allow, pic_amount, p_details, unuse_favorite, like_limit = find_user_settings(ctx.message.author.id)
                
                r18switch = r18allow and global_r18switch

                rng = random.randint(0, len(favorite) - 1)

                loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc)) 

                search_results = main_related(favorite[rng], pic_amount, r18switch)

                await loading_screen.delete()

                if search_results != None and search_results != []:
                    found = True

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
                        message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                        if p_details == True:
                            message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                            message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                        files=[                    
                            discord.File(loading_picture + ".jpg")
                            ,discord.File("Karl_hsiao.png")
                            ]

                        await ctx.send(embed=message, files=files)


                        if os.path.exists(loading_picture + ".jpg"):
                            os.remove(loading_picture + ".jpg")
    
                    return

                else:
                    await ctx.send(embed=discord.Embed(title="No result found."))

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
            message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            await ctx.send(embed=message, files=files)


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
            found = True

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
                message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

                if p_details == True:
                    message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                    message.add_field(name="tags:",value=str(original_tags),inline=False)
    
                files=[                    
                    discord.File(loading_picture + ".jpg")
                       ,discord.File("Karl_hsiao.png")
                    ]

                await ctx.send(embed=message, files=files)


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
    #loading_screen_id = loading_screen.id

    search_results = search_main(search, amount, like_limit, r18switch)
    
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
            message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            await ctx.send(embed=message, files=files)


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

    #like_limit = 3000

    r18switch = (global_r18switch and r18allow)
    loading_picture = "good_pic"

    loading_screen = await ctx.send(embed=discord.Embed(title="Loading picture...",color=0xeeeecc))    
    #loading_screen_id = loading_screen.id

    search_results = search_id_main(search)

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
            message.set_footer(text="Bot made by Karl_hsiao#9522", icon_url="attachment://Karl_hsiao.png")

            if p_details == True:
                message.add_field(name="bookmarks:",value=str(bookmarks),inline=False)
                message.add_field(name="tags:",value=str(original_tags),inline=False)
    
            files=[                    
                discord.File(loading_picture + ".jpg")
                   ,discord.File("Karl_hsiao.png")
                    ]

            await ctx.send(embed=message, files=files)


            if os.path.exists(loading_picture + ".jpg"):
                os.remove(loading_picture + ".jpg")
    
        return

    else:
        await ctx.send(embed=discord.Embed(title="No result found."))

@bot.command(pass_context=True)
async def testing(ctx, *arg):
    n = arg[0]
    await ctx.send(n[3:-1])


    return

@bot.event
async def on_raw_reaction_add(ctx, payload, reaction, user):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    embeds = msg.embeds
    emoji = reaction.emoji

    for embed in embeds:
        print(embed.to_dict())

    if user.bot:
        return

    if emoji == ":heart:":
        await ctx.send("image liked!")
    
bot.run(TOKEN)  
