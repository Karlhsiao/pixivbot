from pixivpy3 import *
from pixiv_functions import *
import pixiv_auth
from downloader import *


tags = []

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

json_result = api.search_illust(word="ナイトメア(アークナイツ)",sort="date_desc")
pixiv_json_result = []
pixiv_urls = []

#print(json_result)

while page != 100:

    for illust in json_result.illusts:
        
        if illust["total_bookmarks"] >= 3000:
            pixiv_json_result.append((illust.title, pixiv_url_fixer(illust), str(illust.total_bookmarks), illust["tags"]))
            pixiv_urls.append(pixiv_url_fixer(illust))
            n += 1

        #print("[%s] %s bookmarks: %s \n tags: %s" % (illust.title, illust.image_urls.medium, str(illust.total_bookmarks), illust["tags"]))

    next_qs = api.parse_qs(json_result.next_url)
    if next_qs == None:
        break
    json_result = api.search_illust(**next_qs)

    page += 1

print("Result found:", n)
with open("test_file.json", "w") as fhandle:
    json.dump(pixiv_json_result, fhandle, indent=4)

for i in pixiv_urls:
    downloader(i, "! nightmare_" + str(x).zfill(4))
    x += 1
