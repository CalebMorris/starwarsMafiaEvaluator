from sets import Set

class StarWarsMafiaGameState():
    def __init__(self, playerList):
        self.players = playerList
        self.isOver = False
        # None, 0, positive, negative
        self.winState = None
        self.killerStates = {x:1 for x in StarWarsSets.activeKillers.intersection(self.players)}

    def evaluateEndConditions(self):
        '''
            If 'Good' wins: positive
            If 'Bad' wins: negative
            0 for stalemate
            None if the game is still going
        '''
        if (self.players == None or len(self.players) == 0):
            self.isOver = True
            self.winState = 0
        elif (len(StarWarsSets.sith.intersection(self.players)) == 0):
            self.isOver = True
            self.winState = len(StarWarsSets.good.intersection(self.players))
        else:
            if (len(StarWarsSets.good.intersection(self.players)) == 0):
                self.isOver = True
                self.winState = -1
        return self.winState

class StarWarsSets():
    good = Set(['ewok', 'obi', 'leia', 'han', 'ackbar', 'yoda', 'luke', 'bathan'])
    bad = Set(['bounty', 'storm', 'probe', 'ev'])
    sith = Set(['emperor', 'darth'])
    eaters = Set(['chewbacca', 'rancor'])
    shooters = Set(['han', 'bounty'])
    activeKillers = eaters.union(shooters).union(Set('bathan'))
    nightKillers = sith.union(Set(['luke', 'bathan']))
