from bs4 import BeautifulSoup
from requests import get
from PIL import Image
import urllib.request
import shutil
import os


uinput = input("Enter NH code / link:  ")

try: 
    uinput = int(uinput)
    link = f"https://nhentai.net/g/{uinput}"
except ValueError:
    link = uinput

page = get(link).text
soup = BeautifulSoup(page, "html.parser")
title = soup.find("div", {"id" : "info"}).h1.text
totalPages = len(soup.find_all("div", {"class" : "thumb-container"}))

print(f"\nDownloading {title}")
dir = f"Downloads/{title}"
os.makedirs(dir)

for i in range(1, totalPages+1):
    imgData = get(f"{link}/{i}").text
    parsed = BeautifulSoup(imgData, "html.parser")
    imgDdl = parsed.find("section", {"id" : "image-container"}).img["src"]
    urllib.request.urlretrieve(imgDdl, f"{dir}/{i}")

print("\nCreating PDF. Please wait")
imgList = []
for i in range(1, totalPages+1):
    imgList.append(Image.open(f"{dir}/{i}"))
imgList[0].save(f"Downloads/{title}.pdf", "PDF", resolution = 100.0, save_all = True, append_images = imgList[1:])

print("\nCleaning up.")
shutil.rmtree(dir)
