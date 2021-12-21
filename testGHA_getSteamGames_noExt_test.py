#! python3
import unittest
import getSteamGames as gS
        
class testSteamGames(unittest.TestCase):
        
    def test_getCommon(self):
        games1=['abcd','bacd','badc','cabd']
        games2=['abcd','bdcd','badc','dabd']
        common=gS.getCommon(games1,games2)
        self.assertEqual(common, ['abcd','badc'])

    def test_gameLink(self):
        appNum = 1234
        link = "<a href=https://store.steampowered.com/app/1234>"
        self.assertEqual(gS.gameLink(appNum), link)

        
if __name__ == '__main__':
    unittest.main()
