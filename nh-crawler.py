from bs4 import BeautifulSoup
from requests import get
import urllib.request
import os
import img2pdf
from PIL import Image

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
pdf_path = "Downloads/nh-converter"
pdf_bytes = img2pdf.convert(dir)
file = open(pdf_path, "wb")
file.write(pdf_bytes)
dir.close()
file.close()

for i in range(1, totalPages+1):
    imgData = get(f"{link}/{i}").text
    parsed = BeautifulSoup(imgData, "html.parser")
    imgDdl = parsed.find("section", {"id" : "image-container"}).img["src"]
    urllib.request.urlretrieve(imgDdl, f"{dir}/{i}")
