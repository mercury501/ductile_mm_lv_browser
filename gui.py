from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
import os
import pickle
from PIL import ImageTk, Image
import zipfile
import wget
import time


lbl = [None for a in range(100)]
here = os.path.dirname(os.path.abspath(__file__))

downloaded_indexes = []
download_prefix = 'https://tinfoil.io/MarioMaker/Download/'
levdownloaded = []

with open(os.path.join(here, "levelnames.pickle"), "rb") as fp:
    levelnames = pickle.load(fp)

with open(os.path.join(here, "levelnumbers.pickle"), "rb") as fp:
    levelnumbers = pickle.load(fp)

with open(os.path.join(here, "levelikes.pickle"), "rb") as fp:
    levelikes = pickle.load(fp)

try:
    with open(os.path.join(here, "levdownloaded.pickle"), "rb") as fp:
        levdownloaded = pickle.load(fp)
except:
    print("no such file")


class MyWindow:
    page_selected = 0
    entry_highl = 0
    selected_lv = []
    downloaded = 0
    just_downloaded = []
    
    page_sel_sel = 0
    
    def __init__(self, win):

        
        
        

        self.del_sel=Button(win, text='Delete Selected')
        self.del_sel.bind('<Button-1>', self.remove_selected)
        self.del_sel.place(x = 100, y = 750)

        self.download_btn=Button(win, text='DOWNLOAD', fg = 'red')
        self.download_btn.bind('<Button-1>', self.download)
        self.download_btn.place(x = 20, y = 750)

        self.pagefwd=Button(win, text='Page -->')
        self.pagefwd.bind('<Button-1>', self.pageplus_sel)
        self.pagefwd.place(x = 270, y = 750)
        
        self.pagebck=Button(win, text='<-- Page')
        self.pagebck.bind('<Button-1>', self.pageminus_sel)
        self.pagebck.place(x = 200, y = 750)

        self.pagefwd=Button(win, text='Page -->')
        self.pagefwd.bind('<Button-1>', self.pageplus)
        self.pagefwd.place(x = 1100, y = 750)
        
        self.pagebck=Button(win, text='<-- Page')
        self.pagebck.bind('<Button-1>', self.pageminus)
        self.pagebck.place(x = 920, y = 750)

        self.addsel=Button(win, text='Add Selected')
        self.addsel.bind('<Button-1>', self.addselected)
        self.addsel.place(x = 1000, y = 750)

        self.pagefwd=Button(win, text='Scrape')
        self.pagefwd.bind('<Button-1>', self.scrape)
        self.pagefwd.place(x = 700, y = 750)
        
        self.updateui(1)
        self.updateicon(1)



    def remove_selected(self, value):
        for l in range(0, len(self.selected_lv)):
            print(here + "/icons/" + levelnumbers[int(self.selected_lv[l])] + ".jpg")
            os.remove(here + "/icons/" + levelnumbers[int(self.selected_lv[l])] + ".jpg" )

        for k in range(len(self.selected_lv)):
            levdownloaded.append(int(levelnumbers[self.selected_lv[k]]))

        for b in range(len(self.selected_lv) - 1, 0 - 1, -1):
            levelnames.pop(self.selected_lv[b])
            levelnumbers.pop(self.selected_lv[b])
            levelikes.pop(self.selected_lv[b])
        self.updateui(1)
        


        with open(os.path.join(here, "levdownloaded.pickle"), "wb") as fp:   
            pickle.dump(levdownloaded, fp)   
        with open(os.path.join(here, "levelikes.pickle"), "wb") as fp:   
            pickle.dump(levelikes, fp) 
        with open(os.path.join(here, "levelnames.pickle"), "wb") as fp:   
            pickle.dump(levelnames, fp) 
        with open(os.path.join(here, "levelnumbers.pickle"), "wb") as fp:   
            pickle.dump(levelnumbers, fp) 
        '''
        for l in range(len(self.selected_lv)):
            self.selected_lv.pop(0)
        '''
        
    
    def download(self, value):
        for i in range(len(self.selected_lv)):
            wget.download(download_prefix + str(levelnumbers[self.selected_lv[i]]), here + '/save/' + str(i) + '.zip')
        for j in range(len(self.selected_lv)):
            with zipfile.ZipFile(here + '/save/' + str(j) + '.zip', 'r') as zip_ref:
                zip_ref.extractall(here + '/save/')
                os.rename(here + '/save/course_data_000.bcd', here + '/save/course_data_' + str(f'{(j + 1):03}') + '.bcd')
                os.rename(here + '/save/course_thumb_000.btl', here + '/save/course_thumb_' + str(f'{(j + 1):03}') + '.btl')
        for k in range(len(self.selected_lv)):
            os.remove(here + '/save/' + str(k) + '.zip')

        #uploading to the switch
        #os.system('transfer_levels.py')



        self.remove_selected(1)

        

        


    def addselected(self, value):
        temp_t = self.lb.curselection()
        temp_l = list(temp_t)
        temp_f = []

        for a in range(len(temp_l)):
            temp_l[a] = int(temp_l[a]) + (40 * self.page_selected)

        for b in range(len(temp_l)):
            if temp_l[b] not in self.selected_lv:
                temp_f.append(temp_l[b])

        self.selected_lv.extend(temp_f)
        self.updateui(1)
        

    def updateicon(self, value):
        icon_num = self.lb.index(ACTIVE) + (self.page_selected * 40)
        self.img = ImageTk.PhotoImage(Image.open(here + "/icons/" + str(levelnumbers[icon_num]) + ".jpg"))  #---------------------------------------
        thumbnail = Label(window, image = self.img)
        thumbnail.place(x = 20, y = 20)

        
      
    def updateui(self, value):
        self.lb=Listbox(window, height=40,width = 80, selectmode='multiple')   #list of available levels
        for a in range(40):
            self.lb.insert(END,levelnames[a + (40 * self.page_selected)])
        self.lb.place(x=700, y=50)
        self.lb.focus_set()
        self.lb.bind('<KeyRelease-Down>', self.updateicon )
        self.lb.bind('<KeyRelease-Up>', self.updateicon )
        self.lb.bind('<Left>', self.pageminus )
        self.lb.bind('<Right>', self.pageplus )

        self.slb=Listbox(window, height=20,width = 80, selectmode='multiple')  #list of selected items
        for a in range(len(self.selected_lv)):
            self.slb.insert(END,levelnames[self.selected_lv[a]])
        self.slb.place(x=50, y=400)

        self.sel=Combobox(window, values=self.selected_lv)
        self.sel.place(x = 540, y = 400)

        #self.num_downlded = Label(window, text = str(self.downloaded), fg = 'blue', font=("Helvetica", 12))
        #self.num_downlded.place(x = 20, y = 730)

        self.currentpage = Label(window, text = str(self.page_selected), fg = 'blue', font=("Helvetica", 12))
        self.currentpage.place(x = 1100, y = 700)

        self.currentpage_sel = Label(window, text = str(self.page_sel_sel), fg = 'blue', font=("Helvetica", 12))
        self.currentpage_sel.place(x = 350, y = 750)

        self.num_sel = Label(window, text = str(len(self.selected_lv)), fg = 'blue', font=("Helvetica", 12))
        self.num_sel.place(x = 550, y = 450)

        

    def scrape(self, value):
        os.system('tinfoilmmscraper.py')
        print('Done Scraping!')

        
    def pageplus(self, value):
        self.page_selected = self.page_selected + 1
        self.updateui(1)
        self.updateicon(1)
        #print(self.page_selected)

    def pageminus(self, value):
        self.page_selected = self.page_selected - 1
        self.updateui(1)
        self.updateicon(1)
        #print(self.page_selected)

    def pageplus_sel(self, value):
        self.page_sel_sel = self.page_sel_sel + 1
        self.updateui(1)
        

    def pageminus_sel(self, value):
        self.page_sel_sel = self.page_sel_sel - 1
        self.updateui(1)
        
        


window=Tk()
mywin=MyWindow(window)

window.title('ductile')
window.geometry("1200x800+10+10")
window.mainloop()
