import urllib.request
import requests
import shutil



def downloader(link, name):

    urls = list()
    urls.append(link)

    for url in urls:
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(str(name) + ".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            print("Ero hassei! please try again")
            continue

if __name__ == "__main__":
    link = input("Enter a pic link: ")
    name = input("Enter picture name: ")
    downloader(link, name)
