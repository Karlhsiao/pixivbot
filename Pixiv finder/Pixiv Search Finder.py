from pixivpy3 import *
from pixiv_functions import *
import pixiv_auth
from downloader import *
import random
from time import sleep
from pixiv_search import *

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

json_result = api.user_bookmarks_illust("57233775")
pixiv_json_result = []
pixiv_urls = []

'''
while page != 100:

    for illust in json_result.illust:
        
        #if illust["total_bookmarks"] >= 3000:
        #pixiv_json_result.append((illust.title, pixiv_url_fixer(illust), str(illust.total_bookmarks), illust["tags"]))
        pixiv_json_result.append(illust)
            #pixiv_urls.append(pixiv_url_fixer(illust))
        n += 1

        #print("[%s] %s bookmarks: %s \n tags: %s" % (illust.title, illust.image_urls.medium, str(illust.total_bookmarks), illust["tags"]))

    next_qs = api.parse_qs(json_result.next_url)
    if next_qs == None:
        break
    json_result = api.user_bookmarks_illust(**next_qs)

    page += 1

print("Result found:", n)
with open("test_file.json", "w") as fhandle:
    json.dump(pixiv_json_result, fhandle, indent=4)
'''
def counter(keyword, like_limit, r18allow):
    json_result = api.search_illust(keyword, sort='popular_desc')
    counter = 0
    exception = 0
    
    while True:

        for illust in json_result.illusts:

            original_tags, translated_tags = tag_fixer(illust.tags)

            print(illust.total_bookmarks, like_limit, exception)

            if illust.total_bookmarks >= like_limit:  

                if r18allow or ("R-18" not in original_tags):
   
                    counter += 1
                    if counter >= 10:
                        return counter

            exception += 1

            if exception > 10000:
                return counter, exception

            elif exception % 500 == 0:
                sleep(0.1)

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            return counter, exception

        json_result = api.search_illust(**next_qs)

                    
            
            
'''
def search_main(keyword, need, like_limit, r18allow):

    json_result = api.search_illust(keyword)
    have = 0
    result = []
    pic_pos = []
    pic_need = 0
    x = 0
    counts, exception = counter(keyword, like_limit, r18allow)


    if counts >= need:
        pic_need = need

    else:
        pic_need = counts


    while x < pic_need:
        n = random.randint(1, exception)

        if n in pic_pos:
            continue

        pic_pos.append(n)
        x += 1

    print(pic_pos)
        
    while True:

        for illust in json_result.illusts:

            picture_url = pixiv_url_fixer(illust)
            original_tags, translated_tags = tag_fixer(illust.tags)

            if illust.total_bookmarks >= like_limit:

                if r18allow or ("R-18" not in original_tags):

                    result.append((illust.title, picture_url, illust.total_bookmarks, original_tags, illust.id))
                    have += 1

                    if have == need:
                        return result

        next_qs = api.parse_qs(json_result.next_url)

        if next_qs == None:
            print("have", have)
            return result

        json_result = api.search_illust(**next_qs)
'''

if __name__ == "__main__":
    #print("Result found: ", counter("ナイチンゲール(アークナイツ)", 3000, True))
    x = 0


    results = search_main("Gawr Gura", 10, 3000, False)

    for i in results:
        pixiv_urls.append(i[1])

    #for i in pixiv_urls:
        
        #downloader(i, "! nightmare_" + str(x).zfill(4))
        #print(x, "success downloaded")
        #x += 1

    with open("test_file.json", "w") as fhandle:
        json.dump(results, fhandle, indent=4)


    #results = search_main("hololive", 10,  5000, False)
    #if results != None:
        #for result in results:

            #title = result[0]
            #pic_url = result[1]
            #bookmarks = result[2]
            #original_tags = result[3]
            #id = result[4]

            #info_printer(title, pic_url, bookmarks, original_tags, id)

        #print("Result found: ", counter("ナイトメア(アークナイツ)", 0, True))
    #else:
        #print("no result")


'''

tags = []

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
'''

'''
def test():
    a = 1
    b = 2
    c = 3
    d = 4
    return a, b, c, d

a, b, c, d = test()

print(a, c)
'''