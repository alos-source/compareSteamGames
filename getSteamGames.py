#! python3

import logging, re#, bs4, requests, sys
logging.basicConfig(filename="steamGames.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s)")

logging.debug("Start of programm")

pfad = "steamHTML\\" # all steam-user HTML-Files should be placed in this directory
dateiname1="SteamGames1.html"
dateiname2="SteamGames2.html"
dateiname3="SteamGames3.html"

datei1 = pfad+dateiname1
datei2 = pfad+dateiname2
datei3 = pfad+dateiname3

# Create Games-Array by STEAM-User HTML File
def getGamesIDs(PATH):

    try:
        with open(PATH,encoding="utf8") as f:
            text = f.read()
    except IOError:
        print("File not accessible")
              
    games = ([])
    games = re.findall("game_\d\d\d+", text)
    logging.debug("Start: "+PATH)
    logging.debug(games)
    logging.info(PATH+" Number of games from IDs: "+str(len(games)))
    logging.debug("Finished "+PATH)
    return games

# Create Games-Array by STEAM-User HTML File
def getGamesNames(PATH):
    
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
    logging.debug("Start: "+PATH)
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

common_games1 = ([])
common_games2= ([])

# Read game lists for three players
gamesNames1 = getNames(getGamesNames(datei1))
gamesIDs1 = getGamesIDs(datei1)
gamesNames2 = getNames(getGamesNames(datei2))
gamesIDs2 = getGamesIDs(datei2)
gamesNames3 = getNames(getGamesNames(datei3))
gamesIDs3 = getGamesIDs(datei3)

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

logging.debug("End of program")

