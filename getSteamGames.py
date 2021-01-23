import bs4, re, requests, sys

pfad = "steamHTML\\" # all steam-user HTML-Files should be placed in this directory
dateiname1="SteamGames1.html"
dateiname2="SteamGames2.html"
dateiname3="SteamGames3.html"

datei1 = pfad+dateiname1
datei2 = pfad+dateiname2
datei3 = pfad+dateiname3

# Create Games-Array by STEAM-User HTML File
def getGames(PATH):

    in_file = open(PATH,"r",encoding="utf8")
    text = in_file.read()
    soup = bs4.BeautifulSoup(text, "html.parser")
    in_file.close()
        
    games = ([])
    games = re.findall("game_\d\d\d+", text)
    return games

# Compare two game-sets and create a set of matching games
def getCommon(games1, games2):
    common_games = ([])
    for game1 in games1:
        for game2 in games2:
            if (game2 == game1):
                #print ("append: "+game1)
                common_games.append(game1)
    return common_games

# extract IDs from "game_ID"-String 
def getIDs(games):
    gameIDs=([])
    for game in games:
        gameIDs.append(game[5:])
    #print (game)
    return gameIDs

# create link to SteamStore from GameID
def gameLink(NUMBER):
    NUMBER = str(NUMBER)
    return """<a href="https://store.steampowered.com/app/"""+NUMBER+">"""

common_games1 = ([])
common_games2= ([])

# Read game lists for three players
games1 = getGames(datei1)
games2 = getGames(datei2)
games3 = getGames(datei3)

# Find matches
common_games1 = getCommon(games1, games2)
#print (common_games1)
common_games2 = getCommon(games3,common_games1)

print (getIDs(common_games2))

