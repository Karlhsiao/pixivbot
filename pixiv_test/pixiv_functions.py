import pixiv_auth
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