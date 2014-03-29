from sets import Set

class StarWarsMafiaGameState():
    def __init__(self, newPlayerList=None, otherState=None):
        '''
            players : list(string) : list of players
            isOver : bool : 
            winState : Maybe int : None, 0, positive, negative
            killerStates : dict{player:int} : has a killer with a one time ability used it
            protectedPlayer : Maybe string : Yoda has protect this player. Lasts until day
            playersToDie : list(string) : Series of players to die to allow for atomicness of night
             as well as the procedural eval when daytime is reached
            disabledPlayer : Maybe string : EV disables a player. Stops eaters and shooters during
             daytime evaluation.
        '''
        if otherState is None:
            if newPlayerList is None:
                self.players = []
            else:
                if 'storm' not in newPlayerList:
                    self.players = newPlayerList
                else:
                    self.players = [x for x in newPlayerList if x != 'storm']
                    self.players.append('storm')
            self.isOver = False
            self.killerStates = {x:1 for x in StarWarsSets.activeKillers.intersection(self.players)}
            self.winState = None
            self.protectedPlayer = None
            self.playersToDie = []
            self.disabledPlayer = None
            self.occurences = 1
            self.resurectStorm = False
        else:
            self.isOver = otherState.isOver
            self.winState = otherState.winState
            self.killerStates = otherState.killerStates.copy()
            self.protectedPlayer = otherState.protectedPlayer
            self.disabledPlayer = otherState.disabledPlayer
            self.playersToDie = [x for x in otherState.playersToDie]
            self.occurences = otherState.occurences
            self.resurectStorm = otherState.resurectStorm
            if newPlayerList is None:
                if 'storm' not in otherState.players:
                    self.players = otherState.players
                else:
                    self.players = [x for x in otherState.players if x != 'storm']
                    self.players.append('storm')
            else:
                if 'storm' not in newPlayerList:
                    self.players = newPlayerList
                else:
                    self.players = [x for x in newPlayerList if x != 'storm']
                    self.players.append('storm')
        self.evaluateEndConditions()

    def __iter__(self):
        return iter(self.players)

    def __eq__(self, other):
        return self.players == other.players and self.killerStates == other.killerStates and\
               self.protectedPlayer == other.protectedPlayer and self.playersToDie == other.playersToDie

    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6}".format(self.occurences, self.players, self.killerStates, self.winState, self.playersToDie, self.protectedPlayer, self.isOver, self.resurectStorm)

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
        elif len(StarWarsSets.sith.intersection(self.players)) == 0:
            self.isOver = True
            self.winState = len(StarWarsSets.good.intersection(self.players))
        else:
            if len(StarWarsSets.good.intersection(self.players)) == 0:
                self.isOver = True
                self.winState = -1
        for activeKiller in self.killerStates.keys():
            if activeKiller not in self.players:
                self.killerStates.pop(activeKiller, None)
        return self.winState

class StarWarsSets():
    sith = Set(['emperor', 'darth'])
    good = Set(['ewok', 'obi', 'leia', 'han', 'ackbar', 'yoda', 'luke', 'bathan', 'chewbacca', 'thermal'])
    bad = sith | Set(['bounty', 'storm', 'probe', 'ev', 'guard', 'rancor'])
    players = good | bad
    eaters = Set(['chewbacca', 'rancor'])
    shooters = Set(['han', 'bounty'])
    activeKillers = eaters | Set(['bathan'])
    nightKillers = sith | Set(['luke', 'bathan', 'thermal'])
    nightSurvivors = Set(['ackbar', 'guard'])
