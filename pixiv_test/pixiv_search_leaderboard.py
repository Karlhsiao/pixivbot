from pixivpy3 import *
import pixiv_auth 
from pixiv_functions import *

api = AppPixivAPI()
refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
access = "bXawE7pjqNlKPQ3iDFnt0ePKbsncJRYXt0tk3SnfMkQ"
api.set_auth(refresh_token=refresh, access_token=access)

tags = []
pics = []

if check_access_token_valid(refresh, access):
    access = access_token_renewer(refresh)
    api.set_auth(refresh_token=refresh, access_token=access)

json_result = api.illust_ranking('day')

for illust in json_result.illusts:
    pic_url = pixiv_url_fixer(illust)  
    pics.append((illust.title, pic_url))
    tags.append((illust.tags))      

n = 0

search = input("Please enter the word you want to search: ")

no_match = True

for pictures in pics:
    original_tags, translated_tags = tag_fixer(tags[n])

    for translated_tag in translated_tags:

        if translated_tag == None:
            continue

        elif search.lower() in translated_tag.lower():

            print("matched tag [%s] %s " % pictures)
            print("tag:", original_tags)
            no_match = False

            break

        elif search.lower() in illust.title:

            print("matched name [%s] %s " % pictures)
            print("tag:", original_tags)
            no_match = False

            break

        elif search.lower() == "":

            print(" p1 [%s] %s " % pictures)
            print("tag:",  original_tags)
            no_match = False

            break
        
    n += 1

if no_match:
        print("No matching result.")
