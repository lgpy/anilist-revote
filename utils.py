import urllib.request
import io
from PIL import Image, ImageTk

def ImgFromUrl(url):
    global image
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    raw_data = response.read()
    im = Image.open(io.BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    return image

def readtoken():
    f = open("AccessToken.dat", "r")
    token = f.read()
    f.close()
    return token

def writetoken(token):
    f = open("AccessToken.dat", "w")
    f.write(token)
    f.close()