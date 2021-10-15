from pixivpy3 import *
from pixiv_functions import *
import pixiv_auth


api = AppPixivAPI()

refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
access = access_token_renewer(refresh)

api.set_auth(refresh_token=refresh, access_token=access)

'''
//Old
tags = []
pics = []
page = 0
no_match = 1

search = input("The word you want to search: ")

json_result = api.search_illust(word=search)



try:

    req = int(input("how many pics you want: "))
    
except:

    req = 100000


try:

    limit_likes = int(input("how many likes you wants to set as limit: "))

except:

    limit_likes = 1000


while True:


    for illust in json_result.illusts:

        n = 0

        pic_url = illust.image_urls.medium
        pic_url = pixiv_url_fixer(pic_url) 

        pics.append((illust.title, pic_url))
        tags.append((illust.tags))


    for pictures in pics:

        original_tags, translated_tags = tag_fixer(tags)

        if illust.total_bookmarks >= limit_likes and page < req:


            print("[%s] %s " % pictures)
            print("tag:", original_tags)
            print("Likes:", illust.total_bookmarks)


            no_match = False

            page += 1

            if page > req:
                break
        n += 1



    next_qs = api.parse_qs(json_result.next_url)
    json_result = api.search_illust(**next_qs)

    if json_result == None:

        break


if no_match:
    print("No matching result.")

    
'''

"""
//Unused counter

def counter(keyword, like_limit, r18allow):
    json_result = api.search_illust(keyword)
    counter = 0
    
    while True:

        for illust in json_result.illusts:


            original_tags, translated_tags = tag_fixer(illust.tags)

            if illust.total_bookmarks >= like_limit:  

                if r18allow or ("R-18" not in original_tags):

                    
                    counter += 1

                    if counter >= 500:
                        return counter

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            return counter

        json_result = api.search_illust(**next_qs)
"""
                    
            
            

def search_main(keyword, need, like_limit, r18allow):

    json_result = api.search_illust(keyword)
    have = 0
    result = []

    while True:

        for illust in json_result.illusts:

            picture_url = pixiv_url_fixer(illust)
            original_tags, translated_tags = tag_fixer(illust.tags)

            if illust.total_bookmarks >= like_limit:  

                if r18allow or ("R-18" not in original_tags):

                    result.append((illust.title, picture_url, illust.total_bookmarks, original_tags, illust.id))
                    have += 1

                    if have == need:
                        print("have", have)
                        return result

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            print("have", have)
            return result

        json_result = api.search_illust(**next_qs)



if __name__ == "__main__":
    search = input("search a word: ")
    results = search_main(search, 10,  5000, False)
    if results != None:
        for result in results:

            title = result[0]
            pic_url = result[1]
            bookmarks = result[2]
            original_tags = result[3]
            id = result[4]

            info_printer(title, pic_url, bookmarks, original_tags, id)

        #print("Result found: ", counter("ナイトメア(アークナイツ)", 5000, False))
    else:
        print("no result")
