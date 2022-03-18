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
    picture_url = pixiv_url_fixer(illust)  
    pics.append((illust.title, picture_url, illust.total_bookmarks, illust.id))
    tags.append((illust.tags))      


def leaderboard_main(search, needs, r18allow):
    needs = int(needs)
    no_match = True
    haves = 0
    result = []

    json_result = api.illust_ranking('day')

    try:
        test = json_result["error"]

        refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
        access = access_token_renewer(refresh)
        api.set_auth(refresh_token=refresh,access_token=access)

        json_result = api.illust_ranking("day")

    except:
        pass
    
    while True:

        for illust in json_result.illusts:

            picture_url = pixiv_url_fixer(illust)  

            original_tags, translated_tags = tag_fixer(illust.tags)

            for translated_tag in translated_tags:

                if translated_tag == None:
                    continue

                elif search.lower() in translated_tag.lower() or search.lower() in illust.title or search == "":

                    if r18allow or ("R-18" not in original_tags):
                        result.append((illust.title, picture_url, illust.total_bookmarks, original_tags, illust.id))

                        no_match = False
                        haves += 1

                        if needs == haves:
                            return result

                        break

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            break

        json_result = api.illust_ranking(**next_qs)

    if no_match:
        print("No matching result.")

    else:
        return result
        
if __name__ == "__main__":
    search = input("Please enter the word you want to search: ")
    needs = int(input("Please enter the number you want: "))

    results = leaderboard_main(search, needs)

    if results != None:
        for result in results:
            info_printer(result[0],result[1],result[2],result[3],result[4])