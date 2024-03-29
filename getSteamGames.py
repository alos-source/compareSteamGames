#! python3
import logging, re #, sys #, bs4, requests, 
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
#import csv
import webbrowser
import locale
import json


configname="config.conf"

files=[]
common_games1 = ([])
common_games2= ([])
config = configname
version = "20210207"
global LANG
LANG = "EN"
global common_games

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
        print("File not accessible: "+PATH)
    
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
        print("File not accessible: "+PATH)
        
    
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
                common_games.append(game1)
    return common_games

# extract IDs from "game_ID"-String 
def getIDs(games):
    gameIDs=([])
    for game in games:
        gameIDs.append(game[5:])
    return gameIDs

# strip Name
def getNames(games):
    gameNames=([])
    for game in games:
        gameNames.append(game[16:-6])
    return gameNames

# create link to SteamStore from GameID
def gameLink(NUMBER):
    NUMBER = str(NUMBER)
    return """<a href=https://store.steampowered.com/app/"""+NUMBER+">"""


def defineFileName(filename):
    filename = askopenfilename()

#def run1():
#    getGamesNames(str(entry_Path1.get()))


def __init__():
    pass

def main():
    #global conf
    conf = {
    "DEBUG" : "INFO",
    "LANG":"",
    "PATH":["./Steam1.html","./Steam2.html","./Steam3.html"]
        }

    logging.basicConfig(filename="steamGames.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s)")

    logging.debug("Start of programm")

    
    # create link to SteamStore from Name
    def searchStore():
        global selectedGame
        global selectedGameName
        NAME = str(common_games[int(selectedGame[1])])
        NAME = selectedGameName
        Search = """https://store.steampowered.com/search/?term="""+NAME+""
        webbrowser.open_new(Search)
    
    def loadConfig():
        try:
            with open(config,encoding="utf8") as f:
                conf = json.load(f)
                confLang = conf.get("LANG")
                confDebug = conf.get("DEBUG")
                confPath = conf.get("PATH")
                logging.debug("config loaded LANG: "+ str(confLang))
                logging.debug("config loaded DEBUG: "+ str(confDebug))
                logging.debug("config loaded Path: "+ str(confPath))                
                #logging.debug("config loaded number: "+ str(len(files)))
                entry_Path1.insert(0,confPath[0])
                entry_Path2.insert(0,confPath[1])
                entry_Path3.insert(0,confPath[2])
                #logging.debug("config loaded: "+ files[0]+ files[1])                                    
        except IOError:
            print("File not accessible"+PATH)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            
    def savePath():
        
        conf["PATH[0]"] = entry_Path1.get()
        conf["PATH[1]"] = entry_Path2.get()
        conf["PATH[2]"] = entry_Path3.get()
        #conf.set("PATH")=confPath
        print(conf["PATH[0]"])
        with open(config, 'w') as f:
            json.dump(conf, f)

#    def save_obj(obj, name ):
#       with open('obj/'+ name + '.pkl', 'wb') as f:
#           pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


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
        global common_games
        common_games = compare(entry_Path1.get(),entry_Path2.get(),entry_Path3.get())
        commonbox.delete(0,tk.END)
        commonbox.bind('<<ListboxSelect>>', cb)
        for game in common_games:
            commonbox.insert('end', game)
        
        label_output['text']= (STRINGS[LANG]["LABELOUTPUT"]+str(len((common_games))))

    def cb(event):
        global selectedGame
        global selectedGameName
        logging.debug(str(event) + '\n' + str(commonbox.curselection()))
        selectedGame = str(commonbox.curselection())
        selectedGameName = commonbox.get(commonbox.curselection())
        button_store["state"] = "normal"

    def select(event):
        i = commonbox.curselection()[0]
        item.set(items[i])
        print(str(event) + '\n' + str(item))

    def callback(event):
        webbrowser.open_new(event.widget.cget("text"))

    global LANG
    global selectedGame
    global selectedGameName

    def getLang():
        localCode = locale.getdefaultlocale()[0]
        logging.debug("OS runnging on: "+localCode)
        logging.debug("LANG: "+localCode[:2])        
        if localCode[:2] == "de": # slice german local code de_DE
            return "DE"
        else:
            return "EN"
    
    def switchLang():
        global LANG
        if LANG == "EN":
            LANG = "DE"
        else:
            LANG = "EN"
        #print("LANG: " + str(LANG))        
        #main_window.update()
        #return LANG
        
        
    STRINGS = {
    
    "DE" :{
                "LANG":"Deutsch",
		"Path":"Pfad",
                "LABELINPUT":"Vergleiche Bibliotheken",
                "LABELOUTPUT":"Gemeinsame Spiele: ",
                "RUN":"Vergleiche",
                "BROWSE":"Öffne Browser"
    },
    "EN":{
                "LANG":"English",
		"Path":"Path",
    		"LABELINPUT":"Compare Libraries",
                "LABELOUTPUT":"Common Games: ",
                "RUN":"Compare",
                "BROWSE":"Open Browser"                
    }
    }
    
    LANG = getLang()
    logging.debug("Language: "+str(STRINGS[LANG]["LANG"]))
    
    # Build GUI
    main_window = tk.Tk()
    main_window.title("SteamGames")
    
    #main_window.iconbitmap(r"media/icon.ico")
    # Grid-Frame for inputs
    frame_input = tk.Frame(main_window)
    frame_input.pack()

    label_input = tk.Label(frame_input, text = STRINGS[LANG]["LABELINPUT"])
    label_input.grid(row = 1, column = 2)
    btn = tk.Button(frame_input,text =(STRINGS[LANG]["Path"]+" 1"), command = open_file1) 
    btn.grid(row = 2, column = 1)
    entry_Path1 = tk.Entry(frame_input)
    entry_Path1.grid(row = 2, column = 2)
    btn2 = tk.Button(frame_input,text =(STRINGS[LANG]["Path"]+" 2"), command = open_file2) 
    btn2.grid(row = 3, column = 1)
    entry_Path2 = tk.Entry(frame_input)
    entry_Path2.grid(row = 3, column = 2)
    btn3 = tk.Button(frame_input,text =(STRINGS[LANG]["Path"]+" 3"), command = open_file3) 
    btn3.grid(row = 4, column = 1)
    entry_Path3 = tk.Entry(frame_input)
    entry_Path3.grid(row = 4, column = 2)
    # Pack-Frame for controls
    frame_buttons = tk.Frame(main_window)
    frame_buttons.pack()
    button_run = tk.Button(frame_buttons, text=STRINGS[LANG]["RUN"], command=runCompare)
    button_run.pack(side= tk.LEFT)
    button_store = tk.Button(frame_buttons, text=STRINGS[LANG]["BROWSE"], command=searchStore, state = "disabled")
    button_store.pack(side= tk.LEFT)
    
    button_lang = tk.Button(frame_buttons, text="SAVE", command=savePath)
    button_lang.pack(side= tk.LEFT)

    # Frame for outputs
    frame_output = tk.Frame(main_window)
    frame_output.pack()
    label_output = tk.Label(frame_output, text=STRINGS[LANG]["LABELOUTPUT"])
    label_output.pack()
    scrollbar = tk.Scrollbar(frame_output, orient="vertical")
    commonbox = tk.Listbox(frame_output,width=50, height=20, yscrollcommand=scrollbar.set)
    scrollbar.config(command=commonbox.yview)
    scrollbar.pack(side="right", fill="y")
    commonbox.pack(side="left",fill=tk.BOTH, expand=True)

    label_footer = tk.Label(main_window,  text=r"https://github.com/alos-source", fg="blue", cursor="hand2")
    label_footer.pack()
    label_footer.bind("<Button-1>", callback)
    label_version = tk.Label(main_window,  text="Version: "+version)
    label_version.pack()


    # Load Values for inputs
    loadConfig()
    
    main_window.mainloop()

# Only run GUI when not called as module
logging.debug("Module run by: "+str(__name__))
if __name__ == "__main__":
    main()
    
logging.debug("End of program")
