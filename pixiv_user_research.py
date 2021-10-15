import json
from pixivpy3 import *
import pixiv_auth
from pixiv_functions import *

tags = []

api = AppPixivAPI()
papi = PixivAPI()

refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
access = "GDPuvBDHpAKkkepEn_MC8jvj04WJQvw7fH468lA4gTE"

api.set_auth(refresh_token=refresh,access_token=access)

try:
    if check_access_token_valid(refresh, access): 
        assert False
except:
    access = access_token_renewer(refresh)
    api.set_auth(refresh_token=refresh,access_token=access)


pixiv_id = "38582538"



def user_main(pixiv_id, keyword="", need=5, r18allow=False):

    json_result = api.user_bookmarks_illust(pixiv_id)
    have = 0
    result = []


    while True:

        for illust in json_result.illusts:

            picture_url = pixiv_url_fixer(illust)
            original_tags, translated_tags = tag_fixer(illust.tags)

            if keyword in original_tags or keyword in translated_tags or keyword == "" or keyword in illust.title: 

                if r18allow or ("R-18" not in original_tags):
 
                    result.append((illust.title, picture_url, illust.total_bookmarks, original_tags, illust.id))
                    have += 1

                    if have == need:
                        return result

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            return result

        json_result = api.user_bookmarks_illust(**next_qs)


if __name__ == "__main__":
    results = user_main(pixiv_id, "",  3)
    if results != None:
        for result in results:

            title = result[0]
            pic_url = result[1]
            bookmarks = result[2]
            original_tags = result[3]
            id = result[4]

            info_printer(title, pic_url, bookmarks, original_tags, id)
    else:
        print("no result")
