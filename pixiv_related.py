from pixivpy3 import *
from pixiv_functions import *


api = AppPixivAPI()
papi = PixivAPI()

refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
access = "GDPuvBDHpAKkkepEn_MC8jvj04WJQvw7fH468lA4gTE"

api.set_auth(refresh_token=refresh,access_token=access)

try:
    check_access_token_expiration = api.user_detail("57233775")
    if check_access_token_expiration.user.account != "karlhsiao": 
        assert False

except:
    access = access_token_renewer(refresh)
    api.set_auth(refresh_token=refresh,access_token=access)


json_result = api.illust_related(85402448)

with open("test_file.json", "w") as fhandle:
    json.dump(json_result, fhandle, indent=4)



def main_related(id, need, r18allow):

    json_result = api.illust_related(id)
    have = 0
    result = []

    while True:

        for illust in json_result.illusts:

            picture_url = pixiv_url_fixer(illust)
            original_tags, translated_tags = tag_fixer(illust.tags)

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

        json_result = api.illust_related(**next_qs)


if __name__ == "__main__":
    id = input("search a id: ")

    results = main_related(id, 5, False)
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


