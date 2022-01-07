from bs4 import BeautifulSoup
from requests import get
import urllib.request
import os


uinput = input("Enter NH code / link:  ")

if len(uinput) == 6:
    link = f"https://nhentai.net/g/{uinput}"
else:
    link = uinput

page = get(link).text
soup = BeautifulSoup(page, "html.parser")
title = soup.find("div", {"id" : "info"}).h1.text
totalPages = len(soup.find_all("div", {"class" : "thumb-container"}))

print(f"Downloading {title}")
dir = f"Downloads/{title}"
os.makedirs(dir)

for i in range(1, totalPages+1):
    imgData = get(f"{link}/{i}").text
    parsed = BeautifulSoup(imgData, "html.parser")
    imgDdl = parsed.find("section", {"id" : "image-container"}).img["src"]
    urllib.request.urlretrieve(imgDdl, f"{dir}/{i}")
