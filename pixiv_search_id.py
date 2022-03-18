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

def search_id_main(id):

    json_result = api.illust_detail(id)

    try:
        test = json_result["error"]

        refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
        access = access_token_renewer(refresh)
        api.set_auth(refresh_token=refresh,access_token=access)

        json_result = api.illust_detail(id)

    except:
        pass

    result = []
    illust = json_result.illust

    picture_url = pixiv_url_fixer(illust)
    original_tags, translated_tags = tag_fixer(illust.tags)

    result.append((illust.title, picture_url, illust.total_bookmarks, original_tags, illust.id))

    return result

def is_id_valid(id):

    json_result = api.illust_detail(id)

    try:
        test = json_result["error"]

        refresh = "WrUovaNgSFjvDx3s0b2Ybe_CqAlprJZsG6bmxTk4aK0"
        access = access_token_renewer(refresh)
        api.set_auth(refresh_token=refresh,access_token=access)

        json_result = api.illust_detail(id)

    except:
        pass

    try:
        if json_result.illust.id == int(id):
            return True

    except:
        return False




if __name__ == "__main__":
    id = input("search a id: ")

    if not is_id_valid(id):
        print("ID not valid!")
        exit()

    results = search_id_main(id)
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


