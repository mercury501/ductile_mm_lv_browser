import requests
import pickle
import os
import sys
#from bs4 import BeautifulSoup
#from selenium import webdriver
#import time
#import PySimpleGUI as sg

#import wget

sys.setrecursionlimit(10000)
here = os.path.dirname(os.path.abspath(__file__))


levelnames = []
levelnumbers = []
levelikes = []

ic_downloaded = 0

currentpage = 1  #current page of tinfoil's web level list

download_prefix = 'https://tinfoil.media/MarioMaker/Download/'  #prefixes to build urls or filter html
icon_prefix = 'https://tinfoil.media/MarioMaker/Thumb/'

url = 'https://tinfoil.media/MarioMaker/'

try:
    with open(os.path.join(here, "levdownloaded.pickle"), "rb") as fp:  #open downloaded level list, to remove them after a new scraping
        levdownloaded = pickle.load(fp)
except:
    print("first time scraping")

if not os.path.isdir('./save'): #create save dir for courses and icons, if they don't already exist
    os.mkdir('./save')
if not os.path.isdir('./icons'):
    os.mkdir('./icons')

 #execute this if scraping, to just download icons it skips this part

r = requests.get('https://tinfoil.media/Api/mml', allow_redirects=True)
open('list.json', 'wb').write(r.content)

#populate levelnames, levelnumbers and levelikes




#remove already downloaded levels from lists

try:
    for h in range(len(levelnames)):
        for k in range(len(levdownloaded)):
            if int(levelnumbers[h]) == levdownloaded[k]:
                levelnames.pop(h)
                levelnumbers.pop(h)
                levelikes.pop(h)

except:print("out range")


with open(os.path.join(here, "levelnames.pickle"), "wb") as fp:   
    pickle.dump(levelnames, fp)

with open(os.path.join(here, "levelnumbers.pickle"), "wb") as fp:   
    pickle.dump(levelnumbers, fp)

with open(os.path.join(here, "levelikes.pickle"), "wb") as fp:   
    pickle.dump(levelikes, fp)

    

   


#download icons for all new levels scraped
for i in range(len(levelnumbers)):
    print("  index: " + str(i) + "  filename: " + str(levelnumbers[i]) )
    if not os.path.isfile(here + "/icons/" + levelnumbers[i] + ".jpg"): 
        wget.download(icon_prefix + str(levelnumbers[i]), here + "/icons/" + levelnumbers[i] + ".jpg" )
        ic_downloaded = ic_downloaded + 1



print("\n")
print("Downloaded courses: " + str(ic_downloaded))




