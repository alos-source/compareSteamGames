#! python3

import logging, re#, bs4, requests, sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import csv


logging.basicConfig(filename="steamGames.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s)")

logging.debug("Start of programm")

pfad = "steamHTML\\" # all steam-user HTML-Files should be placed in this directory
dateiname1="SteamGames1.html"
dateiname2="SteamGames2.html"
dateiname3="SteamGames3.html"
configname="config.cfg"

files=[]
common_games1 = ([])
common_games2= ([])
datei1 = pfad+dateiname1
datei2 = pfad+dateiname2
datei3 = pfad+dateiname3
config = configname
   

# Create Games-Array by STEAM-User HTML File
def getGamesIDs(PATH):
    logging.debug("Start: "+PATH)
    games = ([])
    try:
        with open(PATH,encoding="utf8") as f:
            text = f.read()
            games = re.findall("game_\d\d\d+", text)
            logging.debug(games)
            logging.info(PATH+" Number of games from IDs: "+str(len(games)))
            logging.debug("Finished "+PATH)
    except IOError:
        print("File not accessible")
    
    return games

# Create Games-Array by STEAM-User HTML File
def getGamesNames(PATH):
    logging.debug("Start getGamesNames: "+PATH)
    games = ([])
    userName = ([])
    
    try:
        with open(PATH,encoding="utf8") as f:
            text = f.read()
            userName = re.findall(":: \w+", text) # Select User Name from File
            games = re.findall("""Name ellipsis ">.+""", text) # Pattern contains 14 chars to be in line with following patterns 
            games = games + re.findall("""or_uninstalled">.+""", text) # own games list contains also tags: ellipsis color_uninstalled"
            games = games + re.findall("""color_disabled">.+""", text) # own games list contains also tags: ellipsis color_disabled"
            logging.debug(games)
            logging.info(PATH+" Number of games from "+ str(userName[0]) +" by Names: "+str(len(games)))
    except IOError:
        print("File not accessible")
        
    
    logging.debug("Finished "+PATH)
    return games


def compare(PATH1,PATH2,PATH3):
    # Read game lists for three players
    gamesNames1 = getNames(getGamesNames(PATH1))
    gamesIDs1 = getGamesIDs(PATH1)
    gamesNames2 = getNames(getGamesNames(PATH2))
    gamesIDs2 = getGamesIDs(PATH2)
    gamesNames3 = getNames(getGamesNames(PATH3))
    gamesIDs3 = getGamesIDs(PATH3)

    logging.debug("path3"+ PATH3)
    logging.debug("games3"+ str(getGamesNames(PATH3)))
    
    # Find matches
    common_games1 = getCommon(gamesNames1, gamesNames2)
    common_games1ID = getCommon(gamesNames1, gamesNames2)
    #print (common_games1)
    if PATH3 != "":
        common_games2 = getCommon(gamesNames3,common_games1)
    else:        
        print("File3 not accessible")
        return common_games1
    
    # print ("found games1: ")
    # print ((common_games1))
    logging.info("found common games: " +str(len((common_games2))))
    print ("found common games: " +str(len((common_games2))))
    print ((common_games2))
    #print ("found: "+str(len(common_games2))+"games: "+getNames(common_games2))
    return common_games2


# Compare two game-sets and create a set of matching games
def getCommon(games1, games2):
    common_games = ([])
    for game1 in games1:
        for game2 in games2:
            if (game2 == game1):
                #print ("append: "+game1)
                common_games.append(game1)
    #print('common ended')
    return common_games

# extract IDs from "game_ID"-String 
def getIDs(games):
    gameIDs=([])
    for game in games:
        gameIDs.append(game[5:])
    #print (game)sis color_disabled
    return gameIDs

# strip Name
def getNames(games):
    gameNames=([])
    for game in games:
        gameNames.append(game[16:-6])
    #print (game)
    return gameNames

# create link to SteamStore from GameID
def gameLink(NUMBER):
    NUMBER = str(NUMBER)
    return """<a href="https://store.steampowered.com/app/"""+NUMBER+">"""


def defineFileName(filename):
    filename = askopenfilename()

def run1():
    getGamesNames(str(entry_Path1.get()))


def __init__():
    pass

def main():
    
    def loadConfig():
        try:
            with open(config,encoding="utf8") as f:
                csvReader = csv.reader(f)
                for row in csvReader:
                    files.append(row[0])
                logging.debug("config loaded: "+ files[0]+ files[1])
                entry_Path1.insert(0,files[0])
                entry_Path2.insert(0,files[1])
                entry_Path3.insert(0,files[2])
        except IOError:
            print("File not accessible")

    def open_file1():
        name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
        print (name)
        
        entry_Path1.delete(0,tk.END)
        entry_Path1.insert(0,name)

    def open_file2():
        name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
        print (name)

        entry_Path2.delete(0,tk.END)
        entry_Path2.insert(0,name)

    def open_file3():
        name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
        print (name)

        entry_Path3.delete(0,tk.END)    
        entry_Path3.insert(0,name)
        
    def runCompare():
        common_games = compare(entry_Path1.get(),entry_Path2.get(),entry_Path3.get())
        commonbox.delete(0,tk.END)
        commonbox.bind('<<ListboxSelect>>', cb)
        for game in common_games:
            commonbox.insert('end', game)
        
        label_output['text']= ("List of common games: "+str(len((common_games))))

    def cb(event):
        logging.debug(str(event) + '\n' + str(commonbox.curselection()))

    def select(event):
        i = commonbox.curselection()[0]
        item.set(items[i])
        print(str(event) + '\n' + str(item))

    
    # Build GUI
    main_window = tk.Tk()
    main_window.title("SteamGames")
    # Grid-Frame for inputs
    frame_input = tk.Frame(main_window)
    frame_input.pack()

    label_input = tk.Label(frame_input, text = "Compare Steam Libraries ")
    label_input.grid(row = 1, column = 2)
    btn = tk.Button(frame_input,text ='Path1', command = open_file1) 
    btn.grid(row = 2, column = 1)
    entry_Path1 = tk.Entry(frame_input)
    entry_Path1.grid(row = 2, column = 2)
    btn2 = tk.Button(frame_input,text ='Path2', command = open_file2) 
    btn2.grid(row = 3, column = 1)
    entry_Path2 = tk.Entry(frame_input)
    entry_Path2.grid(row = 3, column = 2)
    btn3 = tk.Button(frame_input,text ='Path3', command = open_file3) 
    btn3.grid(row = 4, column = 1)
    entry_Path3 = tk.Entry(frame_input)
    entry_Path3.grid(row = 4, column = 2)
    # Pack-Frame for controls
    frame_buttons = tk.Frame(main_window)
    frame_buttons.pack()
    button_add = tk.Button(frame_buttons, text="run", command=runCompare)
    button_add.pack(side= tk.LEFT)
    # Frame for outputs
    frame_output = tk.Frame(main_window)
    frame_output.pack()
    label_output = tk.Label(frame_output, text="List of common games: ")
    label_output.pack()
    scrollbar = tk.Scrollbar(frame_output, orient="vertical")
    commonbox = tk.Listbox(frame_output,width=50, height=20, yscrollcommand=scrollbar.set)
    scrollbar.config(command=commonbox.yview)
    scrollbar.pack(side="right", fill="y")
    commonbox.pack(side="left",fill=tk.BOTH, expand=True)
    # Load Values for inputs
    loadConfig()
    

# Only run GUI when not called as module
logging.debug("Module run by: "+str(__name__))
if __name__ == "__main__":
    main()
    
logging.debug("End of program")
