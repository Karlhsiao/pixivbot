from pixivpy3 import *
from pixiv_functions import *
import pixiv_auth
from downloader import *
import random
from time import sleep

api = AppPixivAPI()
papi = PixivAPI()

def renew_access_token(refresh_token):
    access_token = pixiv_auth.refresh(refresh_token)
    return access_token

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

page = 0
n = 0
x = 1

json_result = api.search_illust("hololive")
pixiv_json_result = []
pixiv_urls = []


with open("test_file.json", "w") as fhandle:
    json.dump(json_result, fhandle, indent=4)
