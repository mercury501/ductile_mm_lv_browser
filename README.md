# ductile mm level browser
scraper for mario maker levels on tinfoil.io

It downloads course names and icons.

Run gui.py to scrape automatically, select from the list on the right, add selected to the list on the left and download.
Use arrows to navigate levels/pages of levels.
Downloaded courses are added to a list to ignore them in the future, and files are in the "save" directory, import them in your savefile with yur app of choice.
Delete selected button will mark selected levels as downloaded, so they won't show up in the future.

Known quirks/bugs: 
After every download it will remove downloaded levels, so the selected list will have random levels in it. Just restart the program to select and download more.
You can go negative with level pages. Don't.

This is still a work in progress, but the leveldownloaded.pickle file is the one with the courses id you downloaded, even in future updates if you have that you won't (shouldn't) lose any data.

# Python dependencies:
run: pip install -r requirements.txt


# TODO
Avoid having to install python dependencies, remove bugs, auto FTP on the console, play mario.
