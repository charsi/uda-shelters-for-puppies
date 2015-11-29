import urllib
import json
import requests

numberOfImages = 141
validateUrls = True


def imgExists(path):
    r = requests.head(path)
    if (
        r.status_code == requests.codes.ok and
        r.headers['content-type'] == 'image/jpeg'
    ):
        return True
    else:
        return False


def getPuppyPic():
    apiUrl = "http://www.thepuppyapi.com/puppy"
    response = urllib.urlopen(apiUrl)
    data = json.loads(response.read())
    return data['puppy_url']

imgs = []

while(len(imgs) < numberOfImages):
    try:
        url = getPuppyPic()
        if url.find('ebay') != -1:
            continue
        if validateUrls:
            if not imgExists(url):
                continue
        imgs.append('"'+url+'"')
        print str(len(imgs))+" image URLs fetched so far.."
        print str(url)
    except requests.exceptions.RequestException as e:
        print e

file = open('images.txt', 'w')
urls = "["+(", ".join(imgs))+"]"
file.write(urls)
file.close()

print "done"
