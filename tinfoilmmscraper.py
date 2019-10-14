import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle
import os
#import PySimpleGUI as sg
import sys
import wget

sys.setrecursionlimit(10000)
here = os.path.dirname(os.path.abspath(__file__))

scrape = True

scrape_bydate = False   #not exactly working yet
changed_sorting = False



levelnames = []
levelnumbers = []
levelikes = []

ic_downloaded = 0

levelnames_bd = []
levelnumbers_bd = [] #for the scrape by date, that doesn't currently work
levelikes_bd = []

currentpage = 1  #current page of tinfoil's web level list

good_prefixes = ('<div class = "ticon"', 'bye')
download_prefix = 'https://tinfoil.media/MarioMaker/Download/'  #prefixes to build urls or filter html
icon_prefix = 'https://tinfoil.media/MarioMaker/Thumb/'

url = 'https://tinfoil.media/MarioMaker/'
    
with open(os.path.join(here, "levdownloaded.pickle"), "rb") as fp:  #open downloaded level list, to remove them after a new scraping
    levdownloaded = pickle.load(fp)

if not os.path.isdir('./save'): #create save dir for courses and icons, if they don't already exist
    os.mkdir('./save')
if not os.path.isdir('./icons'):
    os.mkdir('./icons')

if (scrape): #execute this if scraping, to just download icons it skips this part
    driver = webdriver.Chrome(here + '/chromedriver.exe') 
    driver.get(url)   #open root web page

    html = driver.page_source
    soup = BeautifulSoup(html)
    pagenum = soup.find_all('a', class_='paginate_button')
    lastpage = int(float(pagenum[6].contents[0]))  #store number of pages



    for z in range(lastpage):
        html = driver.page_source
        soup = BeautifulSoup(html)
        links = soup.find_all('a', class_='')  #links[].text is levelname, links[].attrs['href'] levelnumber
        #icons = soup.find_all('div', class_='ticon')   #redundant
        likes = soup.find_all('th') #number of likes is in likes[].contents[0]
        
        if scrape_bydate and not changed_sorting:
            dat = driver.find_elements_by_xpath("//*[@id='DataTables_Table_0']/thead/tr/th[11]")[0]#put here the content you have put in Notepad, ie the XPath
            time.sleep(0.2)
            dat.click()
            time.sleep(0.2)
            dat.click()
            changed_sorting = True

        for i in range(3):
            del links[0]
        del links[len(links) - 1]    #remove useless entries, and clean link names

        for i in range(len(links)):
            links[i].attrs['href'] = links[i].attrs['href'][17:]   

        for i in range(13):
            del likes[0]
        del likes[1::2]


        if not scrape_bydate:
            for l in range(len(links)):              #add current page's data to array
                levelnames.append(links[l].text)
                levelnumbers.append(links[l].attrs['href'])
                
                try:
                    levelikes.append(int(likes[l].contents[0]))
                except IndexError:
                    levelikes.append(0) 

        else:
            for l in range(len(links)):              #add current page's data to array
                levelnames_bd.append(links[l].text)
                levelnumbers_bd.append(links[l].attrs['href'])
                
                try:
                    levelikes_bd.append(int(likes[l].contents[0]))
                except IndexError:
                    levelikes_bd.append(0) 

        currentpage = currentpage + 1
        elem = driver.find_elements_by_xpath("//*[@id='DataTables_Table_0_next']")[0]# ie the XPath
        time.sleep(0.2)
        elem.click()
        print("page: " + str(currentpage))

    driver.close() #in the end, close web page

    #remove already downloaded levels from lists
    if not scrape_bydate:
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

    else:
        try:
            for h in range(len(levelnames_bd)):
                for k in range(len(levdownloaded)):
                    if int(levelnumbers_bd[h]) == levdownloaded[k]:
                        levelnames_bd.pop(h)
                        levelnumbers_bd.pop(h)
                        levelikes_bd.pop(h)

        except:print("out range")


        with open(os.path.join(here, "levelnames_bd.pickle"), "wb") as fp:   
            pickle.dump(levelnames_bd, fp)

        with open(os.path.join(here, "levelnumbers_bd.pickle"), "wb") as fp:   
            pickle.dump(levelnumbers_bd, fp)

        with open(os.path.join(here, "levelikes_bd.pickle"), "wb") as fp:   
            pickle.dump(levelikes_bd, fp)


else:    #pickling process ^   V
    
    with open(os.path.join(here, "levelnames.pickle"), "rb") as fp:   
        levelnames = pickle.load(fp)

    with open(os.path.join(here, "levelnumbers.pickle"), "rb") as fp:   
        levelnumbers = pickle.load(fp)

    with open(os.path.join(here, "levelikes.pickle"), "rb") as fp:   
        levelikes = pickle.load(fp)

    #remove already downloaded levels from lists
    try:
        for h in range(len(levelnames)):
            for k in range(len(levdownloaded)):
                if int(levelnumbers[h]) == levdownloaded[k]:
                    levelnames.pop(h)
                    levelnumbers.pop(h)
                    levelikes.pop(h)

    except:print("out range")

    with open(os.path.join(here, "levelnames.pickle"), "wb") as fp:     #save cleaned database
            pickle.dump(levelnames, fp)

    with open(os.path.join(here, "levelnumbers.pickle"), "wb") as fp:   
        pickle.dump(levelnumbers, fp)

    with open(os.path.join(here, "levelikes.pickle"), "wb") as fp:   
        pickle.dump(levelikes, fp)



#download icons for all new levels scraped
for i in range(len(levelnumbers)):
    print("  index: " + str(i) + "  filename: " + str(levelnumbers[i]) )
    if not os.path.isfile(here + "/icons/" + levelnumbers[i] + ".jpg"): 
        wget.download(icon_prefix + str(levelnumbers[i]),here + "/icons/" + levelnumbers[i] + ".jpg" )
        ic_downloaded = ic_downloaded + 1



print("\n")
print("Downloaded courses: " + str(ic_downloaded))




