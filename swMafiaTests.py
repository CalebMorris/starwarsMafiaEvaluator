import unittest
from swMafiaGenerator import *
from starWarsMafiaGameState import *

def joinLists(listTuple):
    return listTuple[0] + listTuple[1]

class noPlayersTests(unittest.TestCase):
    def testDay(self):
        gameStateEmpty = GameState([])
        results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([])))
        self.assertTrue(len(results) == 1)
        self.assertTrue(gameStateEmpty == results[0])
    def testNight(self):
        gameStateEmpty = GameState([])
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState([])))
        self.assertTrue(len(results) == 1)
        self.assertTrue(gameStateEmpty == results[0])

class singlePlayerTests(unittest.TestCase):
    def testDay(self):
        for player in StarWarsSets.players:
            gameStateEmpty = GameState([player])
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([player])))
            self.assertTrue(len(results) == 1)
            self.assertTrue(gameStateEmpty == results[0])
    def testNight(self):
        for player in StarWarsSets.players:
            gameStateEmpty = GameState([player])
            results = joinLists(StarWarsPathEvaluator.nightCycle(GameState([player])))
            self.assertTrue(len(results) == 1)
            self.assertTrue(gameStateEmpty == results[0])

class nightCycleTests(unittest.TestCase):
    def testEmperorAndOneGood(self):
        for player in StarWarsSets.good ^ (StarWarsSets.shooters & StarWarsSets.good) ^ Set(['thermal']) ^ Set(['luke']) ^ Set(['ackbar']):
            results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', player])))
            self.assertTrue(GameState(['emperor']) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'ackbar'])))
        self.assertTrue(GameState(['emperor', 'ackbar']) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal'])))
        self.assertTrue(GameState([]) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'han'])))
        self.assertTrue(GameState([]) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'luke'])))
        self.assertTrue(GameState([]) in results)
        self.assertTrue(GameState(['emperor']) in results)
    def testDarthAndOneGood(self):
        for player in StarWarsSets.good ^ (StarWarsSets.shooters & StarWarsSets.good) ^ Set(['thermal']) ^ Set(['luke']) ^ Set(['ackbar']):
            results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['darth', player])))
            self.assertTrue(GameState(['darth']) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['darth', 'ackbar'])))
        self.assertTrue(GameState(['darth', 'ackbar']) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['darth', 'thermal'])))
        self.assertTrue(GameState([]) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['darth', 'han'])))
        self.assertTrue(GameState([]) in results)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['darth', 'luke'])))
        self.assertTrue(GameState([]) in results)
        self.assertTrue(GameState(['darth']) in results)
    def testEmperorOneGoodAndThermal(self):
        for player in StarWarsSets.good ^ (StarWarsSets.shooters & StarWarsSets.good) ^ Set(['luke']) ^ Set(['thermal']) ^ Set(['yoda']) ^ Set(['bathan']):
            results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal', player])))
            for result in results:
                self.assertTrue(result.winState == 1 or result.winState == None)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal', 'bathan'])))
        self.assertTrue(GameState(['emperor', 'thermal']) in results)
        self.assertTrue(GameState(['thermal']) in results)
        self.assertTrue(GameState([]) in results)
        self.assertTrue(next(i for i in results if i == GameState(['bathan'])).occurences == 3)
        self.assertTrue(len(results) == 4)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal', 'yoda'])))
        self.assertTrue(GameState(['emperor', 'thermal', 'yoda']) in results)
        self.assertTrue(GameState(['emperor', 'yoda']) in results)
        self.assertTrue(next(i for i in results if i == GameState(['emperor', 'thermal'])).occurences == 2)
        self.assertTrue(len(results) == 3)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal', 'han'])))
        self.assertTrue(GameState(['han']) in results)
        self.assertTrue(GameState(['thermal']) in results)
        self.assertTrue(GameState(['emperor']) in results)
        self.assertTrue(len(results) == 3)
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'thermal', 'luke'])))
        self.assertTrue(GameState(['thermal']) in results)
        self.assertTrue(GameState(['emperor', 'thermal']) in results)
        self.assertTrue(next(i for i in results if i == GameState(['luke'])).occurences == 2)
        self.assertTrue(next(i for i in results if i == GameState([])).occurences == 2)
        self.assertTrue(len(results) == 4)
    def testEmperorAndBothShooters(self):
        results = joinLists(StarWarsPathEvaluator.nightCycle(GameState(['emperor', 'bounty', 'han'])))
        self.assertTrue(GameState(['han']) in results)
        self.assertTrue(GameState(['bounty']) in results)
        self.assertTrue(next(i for i in results if i == GameState([])).occurences == 2)
        self.assertTrue(len(results) == 3)

class dayCycleTests(unittest.TestCase):
    def testEmperorAndOneGood(self):
        for player in StarWarsSets.good ^ (StarWarsSets.eaters & StarWarsSets.good):
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState(['emperor', player])))
            self.assertTrue(GameState(['emperor', player]) in results)
        results = joinLists(StarWarsPathEvaluator.dayCycle(GameState(['emperor', 'chewbacca'])))
        self.assertTrue(GameState(['emperor', 'chewbacca']) in results)
        eaterUsedState = GameState(['chewbacca'])
        eaterUsedState.killerStates['chewbacca'] = 0
        self.assertTrue(eaterUsedState in results)
    def testDarthAndOneGood(self):
        for player in StarWarsSets.good ^ (StarWarsSets.eaters & StarWarsSets.good):
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState(['darth', player])))
            self.assertTrue(GameState(['darth', player]) in results)
        results = joinLists(StarWarsPathEvaluator.dayCycle(GameState(['darth', 'chewbacca'])))
        self.assertTrue(GameState(['darth', 'chewbacca']) in results)
        eaterUsedState = GameState(['chewbacca'])
        eaterUsedState.killerStates['chewbacca'] = 0
        self.assertTrue(eaterUsedState in results)
    def testThreePeopleNoShootersOrEaters(self):
        for sith in StarWarsSets.sith:
            for player in StarWarsSets.good ^ Set(['chewbacca']) ^ Set(['han']) ^ Set(['ackbar']):
                for player2 in [x for x in StarWarsSets.players ^ StarWarsSets.shooters ^ StarWarsSets.eaters ^ StarWarsSets.nightSurvivors if x != player and x != sith]:
                    results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, player, player2])))
                    if 'storm' != player2:
                        self.assertTrue(GameState([sith, player]) in results)
                        self.assertTrue(GameState([player, player2]) in results)
                        self.assertTrue(GameState([sith, player2]) in results)
                        self.assertTrue(GameState([sith, player, player2]) in results)
                        self.assertTrue(len(results) == 4)
                    else:
                        self.assertTrue(GameState([player, player2]) in results)
                        self.assertTrue(GameState([sith, player2]) in results)
                        self.assertTrue(GameState([sith, player, player2]) in results)
                        self.assertTrue(next(i for i in results if i == GameState([sith, player, player2])).occurences == 2)
                        self.assertTrue(len(results) == 3)
    def testThreePeopleWithOneShooter(self):
        for sith in StarWarsSets.sith:
            for player in [x for x in StarWarsSets.players ^ StarWarsSets.shooters ^ StarWarsSets.eaters ^ StarWarsSets.nightSurvivors if x != sith]:
                for player2 in StarWarsSets.shooters:
                    results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, player, player2])))
                    if (player in StarWarsSets.good or player2 in StarWarsSets.good):
                        if player != 'storm' and player2 != 'storm':
                            self.assertTrue(GameState([sith]) in results)
                            self.assertTrue(GameState([player]) in results)
                            self.assertTrue(GameState([player, player2]) in results)
                            self.assertTrue(GameState([sith, player2]) in results)
                            self.assertTrue(GameState([sith, player, player2]) in results)
                            self.assertTrue(len(results) == 5)
                        else:
                            self.assertTrue(GameState([player]) in results)
                            self.assertTrue(GameState([player, player2]) in results)
                            self.assertTrue(GameState([sith, player]) in results)
                            self.assertTrue(GameState([sith, player, player2]) in results)
                            self.assertTrue(next(i for i in results if i == GameState([sith, player, player2])).occurences == 2)
                            self.assertTrue(len(results) == 4)
                    else:
                        self.assertTrue(GameState([sith, player, player2]) in results)
                        self.assertTrue(len(results) == 1)
                        
    def testThreePeopleWithTwoShooters(self):
        for sith in StarWarsSets.sith:
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, 'bounty', 'han'])))
            self.assertTrue(GameState([sith, 'bounty', 'han']) in results)
            self.assertTrue(GameState(['bounty', 'han']) in results)
            self.assertTrue(GameState(['han']) in results)
            self.assertTrue(GameState(['bounty']) in results)
            self.assertTrue(GameState([]) in results)
            self.assertTrue(next(i for i in results if i == GameState([])).occurences == 2)
    def testThreePeopleWithOneShooterOneEater(self):
        for sith in StarWarsSets.sith:
            for eater in StarWarsSets.eaters:
                for shooter in StarWarsSets.shooters:
                    results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, eater, shooter])))
                    if eater in StarWarsSets.good or shooter in StarWarsSets.good:
                        self.assertTrue(GameState([sith, shooter]) in results)
                        self.assertTrue(GameState([eater, shooter]) in results)
                        self.assertTrue(GameState([sith]) in results)
                        self.assertTrue(GameState([eater]) in results)
                        eatenGameState = GameState([eater, shooter])
                        eatenGameState.killerStates[eater] = 0
                        self.assertTrue(eatenGameState in results)
                        eatenGameState = GameState([eater])
                        eatenGameState.killerStates[eater] = 0
                        self.assertTrue(eatenGameState in results)
                        self.assertTrue(len(results) == 7)
                        self.assertTrue(next(i for i in results if i == GameState([sith])).occurences == 2)
                    else:
                        self.assertTrue(len(results) == 1)
                    self.assertTrue(GameState([sith, eater, shooter]) in results)
    def testThreePeopleWithTwoEaters(self):
        for sith in StarWarsSets.sith:
            eater1 = 'chewbacca'
            eater2 = 'rancor'
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, eater1, eater2])))
            self.assertTrue(GameState([sith, eater1, eater2]) in results)
            self.assertTrue(GameState([sith, eater1]) in results)
            self.assertTrue(GameState([sith, eater2]) in results)
            self.assertTrue(GameState([eater1, eater2]) in results)
            eatenGameState = GameState([sith, eater1])
            eatenGameState.killerStates[eater1] = 0
            self.assertTrue(eatenGameState in results)
            eatenGameState = GameState([sith, eater2])
            eatenGameState.killerStates[eater2] = 0
            self.assertTrue(eatenGameState in results)
            eatenGameState = GameState([eater1, eater2])
            eatenGameState.killerStates[eater2] = 0
            self.assertTrue(eatenGameState in results)
            eatenGameState = GameState([eater1, eater2])
            eatenGameState.killerStates[eater1] = 0
            self.assertTrue(eatenGameState in results)
            eatenGameState = GameState([eater1])
            eatenGameState.killerStates[eater1] = 0
            self.assertTrue(eatenGameState in results)
            eatenGameState = GameState([eater2])
            eatenGameState.killerStates[eater2] = 0
            self.assertTrue(eatenGameState in results)
            self.assertTrue(len(results) == 10)
    def testThreePeopleWithOneNightSurvivor(self):
        for sith in StarWarsSets.sith:
            for survivor in StarWarsSets.nightSurvivors:
                skipSets = StarWarsSets.players ^ StarWarsSets.shooters ^ StarWarsSets.eaters ^ StarWarsSets.nightKillers ^ StarWarsSets.nightSurvivors
                for player in [x for x in skipSets if x != sith]:
                    results = joinLists(StarWarsPathEvaluator.nightCycle(GameState([sith, survivor, player])))
                    if survivor not in StarWarsSets.bad or player not in StarWarsSets.bad:
                        self.assertTrue(GameState([sith, survivor]) in results)
                        self.assertTrue(GameState([sith, survivor, player]) in results)
                        self.assertTrue(len(results) == 2)
                    else:
                        self.assertTrue(GameState([sith, survivor, player]) in results)
                        self.assertTrue(len(results) == 1)
    def testThreePeopleWithTwoNightSurvivor(self):
        for sith in StarWarsSets.sith:
            survivor = 'ackbar'
            survivor2 = 'guard'
            results = joinLists(StarWarsPathEvaluator.nightCycle(GameState([sith, survivor, survivor2])))
            self.assertTrue(GameState([sith, survivor, survivor2]) in results)
            self.assertTrue(next(i for i in results if i == GameState([sith, survivor, survivor2])).occurences == 2)
            self.assertTrue(len(results) == 1)
    def testTwoEwoks(self):
        for sith in StarWarsSets.sith:
            results = joinLists(StarWarsPathEvaluator.dayCycle(GameState([sith, 'ewok', 'ewok'])))
            self.assertTrue(GameState(['ewok', 'ewok']) in results)
            self.assertTrue(GameState([sith, 'ewok']) in results)
            self.assertTrue(GameState([sith, 'ewok']) in results)
            self.assertTrue(next(i for i in results if i == GameState([sith, 'ewok'])).occurences == 2)
            self.assertTrue(len(results) == 3)
def main():
    unittest.main()

if __name__ == '__main__':
    main()
