import pixiv_auth
import json
from pixivpy3 import *

api = AppPixivAPI()


def tag_fixer(tag):
    tags = []
    translated_tags = []
    for i in tag:
        translated_tags.append(i.get("translated_name"))
        tags.append(i.get("name"))

    return tags, translated_tags

def pixiv_url_fixer(img):
    pic_url = img.image_urls.medium
    pic_url = pic_url.replace("pximg.net","pixiv.cat")
    return pic_url

def access_token_renewer(refresh_token):
    access = pixiv_auth.refresh(refresh_token)
    return access

def check_access_token_valid(refresh, access):
    api.set_auth(refresh_token=refresh, access_token=access)
    user = api.user_detail("57233775")
    try:
        if user["user_id"] == "Karlhsiao":
            return False
        else:
            return True
    except:
        return True

def info_printer(title, pic_url, bookmarks, original_tags, id):
    print("[%s]" % (title))
    print("original link: https://pixiv.net/artworks/" + str(id))
    print("bookmarks: %s" % (str(bookmarks)))
    print("tags:", original_tags)
    print("link: %s" % (pic_url))
    print("")

def turn_page_bookmarks(json_result):
    next_qs = api.parse_qs(json_result.next_url)
    if next_qs == None:
        return None
    json_result = api.user_bookmarks_illust(**next_qs)
    return json_result

def is_number(x):
    try:
        x = int(x)
        return True
    except:
        return False

def find_user_settings(user):
    with open("user_settings.json", "r") as fhandle:
        user_settings = json.load(fhandle)

        for user_id in user_settings:
            try:
                
                if user_id["user"] == user:
                    personal_detail = user_id["personal_detail"]
                    r18allow = user_id["r18allow"]
                    pic_amount = user_id["picture_amount"]
                    p_details = user_id["print_details"]
                    favorite = user_id["favorite"]
                    like_limit = user_id["like_limit"]

                    return personal_detail, r18allow, pic_amount, p_details, favorite, like_limit

            except:
                return False

        return False
