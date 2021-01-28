#! python3

import logging, re#, bs4, requests, sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path


logging.basicConfig(filename="steamGames.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s)")

logging.debug("Start of programm")

pfad = "steamHTML\\" # all steam-user HTML-Files should be placed in this directory
dateiname1="SteamGames1.html"
dateiname2="SteamGames2.html"
dateiname3="SteamGames3.html"

datei1 = pfad+dateiname1
datei2 = pfad+dateiname2
datei3 = pfad+dateiname3
#item = tk.StringVar()

def cb(event):
    print(str(event) + '\n' + str(commonbox.curselection()))

def select(event):
    i = commonbox.curselection()[0]
    item.set(items[i])
    print(str(event) + '\n' + str(item))

# Create Games-Array by STEAM-User HTML File
def getGamesIDs(PATH):
    logging.debug("Start: "+PATH)
    try:
        with open(PATH,encoding="utf8") as f:
            text = f.read()
    except IOError:
        print("File not accessible")
              
    games = ([])
    games = re.findall("game_\d\d\d+", text)
    
    logging.debug(games)
    logging.info(PATH+" Number of games from IDs: "+str(len(games)))
    logging.debug("Finished "+PATH)
    return games

# Create Games-Array by STEAM-User HTML File
def getGamesNames(PATH):
    logging.debug("Start getGamesNames: "+PATH)
        
    try:
        with open(PATH,encoding="utf8") as f:
            text = f.read()
    except IOError:
        print("File not accessible")
    
    userName = re.findall(":: \w+", text) # Select User Name from File
    games = ([])
    games = re.findall("""Name ellipsis ">.+""", text) # Pattern contains 14 chars to be in line with following patterns 
    games = games + re.findall("""or_uninstalled">.+""", text) # own games list contains also tags: ellipsis color_uninstalled"
    games = games + re.findall("""color_disabled">.+""", text) # own games list contains also tags: ellipsis color_disabled"
    
    logging.debug(games)
    logging.info(PATH+" Number of games from "+ str(userName[0]) +" by Names: "+str(len(games)))
    logging.debug("Finished "+PATH)
    return games


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

def askopenfile():
   return askopenfile()

def open_file1():
    name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
    print (name)
    #return name
    #file = askopenfile(title = "Files", filetypes =[('Python Files', '*.docx')]) 
    #if file is not None: 
    #    content = file.read()
    
    
    entry_Path1.insert(0,name)

def open_file2():
    name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
    print (name)
    #return name
    #file = askopenfile(title = "Files", filetypes =[('Python Files', '*.docx')]) 
    #if file is not None: 
    #    content = file.read()
    entry_Path2.insert(0,name)

def open_file3():
    name= askopenfilename(initialdir = "./",title = "Select file",filetypes = (("html-Files","*.html"),("all files","*.*")))
    print (name)
    #return name
    #file = askopenfile(title = "Files", filetypes =[('Python Files', '*.docx')]) 
    #if file is not None: 
    #    content = file.read()
    entry_Path3.insert(0,name)

common_games1 = ([])
common_games2= ([])

def run1():
    getGamesNames(str(entry_Path1.get()))

def runCompare():
    # Read game lists for three players
    gamesNames1 = getNames(getGamesNames(str(entry_Path1.get())))
    gamesIDs1 = getGamesIDs(entry_Path1.get())
    gamesNames2 = getNames(getGamesNames(entry_Path2.get()))
    gamesIDs2 = getGamesIDs(entry_Path2.get())
    gamesNames3 = getNames(getGamesNames(entry_Path3.get()))
    gamesIDs3 = getGamesIDs(entry_Path3.get())

    # Find matches
    common_games1 = getCommon(gamesNames1, gamesNames3)
    common_games1ID = getCommon(gamesNames1, gamesNames2)
    #print (common_games1)
    common_games2 = getCommon(gamesNames2,common_games1)

    # print ("found games1: ")
    # print ((common_games1))
    logging.info("found common games: " +str(len((common_games2))))
    print ("found common games: " +str(len((common_games2))))
    print ((common_games2))
    #print ("found: "+str(len(common_games2))+"games: "+getNames(common_games2))

    commonbox.delete(0,tk.END)
    commonbox.bind('<<ListboxSelect>>', cb)
    for game in common_games2:
        #listboxNamen = Listbox(master=frameListbox, selectmode='browse')
        commonbox.insert('end', game)




# Build GUI
main_window = tk.Tk()
main_window.title("SteamGames")


frame_input = tk.Frame(main_window)
frame_input.pack()


label_input = tk.Label(frame_input, text = "Compare Steam Libraries ")
label_input.pack()

btn = tk.Button(frame_input,text ='Path1', command = open_file1) 
btn.pack(side = tk.LEFT)

entry_Path1 = tk.Entry(frame_input)
entry_Path1.pack(side= tk.LEFT)

btn2 = tk.Button(frame_input,text ='Path2', command = open_file2) 
btn2.pack(side = tk.LEFT)

entry_Path2 = tk.Entry(frame_input)
entry_Path2.pack(side= tk.LEFT)

btn3 = tk.Button(frame_input,text ='Path3', command = open_file3) 
btn3.pack(side = tk.LEFT)

entry_Path3 = tk.Entry(frame_input)
entry_Path3.pack(side= tk.LEFT)


#frame = tk.Frame(main_window)
#frame.pack()
#entry_num1 = tk.Entry(frame)
#entry_num1.pack(side= tk.LEFT)
#entry_num2 = tk.Entry(frame)
#entry_num2.pack(side = tk.LEFT)
#label_action = tk.Label(main_window, text="Select Files")
#label_action.pack()
frame_buttons = tk.Frame(main_window)
frame_buttons.pack()



frame_output = tk.Frame(main_window)
frame_output.pack()



button_add = tk.Button(frame_buttons, text="run", command=runCompare)
button_add.pack(side= tk.LEFT)
button_add1 = tk.Button(frame_buttons, text="read1", command=run1)
button_add1.pack(side= tk.LEFT)
#button_add = tk.Button(frame_buttons, text="-", command=calc_sub)
#button_add.pack(side= tk.LEFT)
#button_add = tk.Button(frame_buttons, text="*", command=calc_add)
#button_add.pack(side= tk.LEFT)
#button_add = tk.Button(frame_buttons, text="/", command=calc_add)
#button_add.pack(side= tk.LEFT)
#label_result = tk.Label(main_window, text="Ergebnis: ")
#label_result.pack()
#entry_result = tk.Entry(main_window)
#entry_result.pack()

# Rahmen Listbox
#frameListbox = tk.Frame(master=main_window, bg='#FFCFC9')
#frameListbox.place(x=5, y=5, width=110, height=80)
#commonbox = Listbox(master=main_window, selectmode='browse')
label_output = tk.Label(frame_output, text="List of common games: ")
label_output.pack()
commonbox = tk.Listbox(frame_output)
commonbox.pack()
#commonbox.place(width=80, height=180)

logging.debug("End of program")

