from starWarsMafiaGameState import StarWarsMafiaGameState as GameState
from starWarsMafiaGameState import StarWarsSets as swSets
from itertools import chain, combinations, permutations
from sets import Set
import math

def betterPrint(gameStateList):
    occSum = sum(y.occurences for y in gameStateList)
    for x in gameStateList:
        print x.__str__(occSum)

def unzip(l, func):
    '''
    func : GameState -> bool
    l : list<GameState>
    Splits l and returns a tuple of (l1, l2) where l1 is all elements of l where func was true and l2 were the remaining
    '''
    if isinstance(l, GameState):
        return unzip([l], func)
    elif type(l) is not list:
        raise TypeError("A list of the wrong type was passed")
    
    l1 = []
    l2 = []
    for element in l:
        if func(element):
            l1.append(element)
        else:
            l2.append(element)
    return (l1, l2)

def unzipGameStates(l):
    return unzip(l, lambda x: x.isOver)

def reduceStates(l):
    '''
    Reduce the number of states in a list by collecting all similar states into a single one with a count on that member
    '''
    if type(l) is not list:
        raise TypeError("A list must be passed")
    if len(l) > 0 and not isinstance(l[0], GameState):
        raise TypeError("The list must be of type %s, but was %s", GameState.__name__, l[0].__class__.__name__)
    reducedList = []
    for x in l:
        if x not in reducedList:
            reducedList.append(x)
        else:
            element = next(i for i in reducedList if i == x)
            element.occurences += x.occurences
    return reducedList

def removeFirst(l, e):
    newList = [x for x in l]
    newList.remove(e)
    return newList

def handleDeath(initialState, nightInNDeaths):
    '''
    Output:
        Returns list of GameStates
    Input:
        initialState: initialGameState. Mainly for the playersToDie
        nightInNDeaths: to keep a shooter from activating Thermal
    '''
    results = []
    if initialState is None:
        raise TypeError("None was passed in place of a GameState")
    elif not isinstance(initialState, GameState):
        raise TypeError("State was of incorrect type. Was of type %s", initialState.__name__)
    if type(nightInNDeaths) is not int:
        raise TypeError("Night counter is of incorrect type. Was %s, but expected %s", type(nightInNDeaths).__name__, int.__name__)
    elif nightInNDeaths < 0:
        raise ValueError("Night counter must be positive. Was %s.", nightInNDeaths)
    if initialState.playersToDie is not None and len(initialState.playersToDie) == 0:
        return [initialState]
    currentPlayerToDie = initialState.playersToDie[0]
    if currentPlayerToDie not in initialState.players:
        initialState.playersToDie.pop(0)
        return handleDeath(initialState, nightInNDeaths - 1)
    if initialState.protectedPlayer == currentPlayerToDie or currentPlayerToDie == 'ackbar' or currentPlayerToDie == 'guard':
        initialState.playersToDie.pop(0)
        results = handleDeath(initialState, len(initialState.playersToDie))
    else:
        newGameState = GameState(newPlayerList = removeFirst(initialState.players, currentPlayerToDie), otherState = initialState)
        newGameState.playersToDie.pop(0)
        remainingPlayersToDie = len(newGameState.playersToDie)
        if currentPlayerToDie not in swSets.shooters or currentPlayerToDie == newGameState.disabledPlayer:
            if nightInNDeaths > 0 and currentPlayerToDie == 'thermal':
                highestSith = 'emperor' if 'emperor' in initialState.players else 'darth'
                newGameState.playersToDie.insert(0, highestSith)
                remainingPlayersToDie += 1
            if currentPlayerToDie == 'storm':
                newGameState.resurectStorm = True
            results = handleDeath(newGameState, remainingPlayersToDie)
        else:
            shooterResults = []
            for player in newGameState.players:
                shooterResponseGameState = GameState(otherState = newGameState)
                shooterResponseGameState.playersToDie.append(player)
                shooterResults += handleDeath(shooterResponseGameState, remainingPlayersToDie)
            results = shooterResults

        for state in results:
            state.evaluateEndConditions()
    return results

class StarWarsPathEvaluator():
    '''
        Evaluation:
        *Death:
            When someone is killed, the possible results/triggers (i.e. bounty dies)
              is evaluated immediately.
            Full example: Sith kill Han-Solo during the night. He shoots someone
              before the day cycle begins.
            After all triggers have been checked, the game state is tested.
              If the game is over then there shouldn't have been any triggers anyway.
    '''
    @staticmethod
    def powerSetPermutations(l):
        for subset in chain.from_iterable(combinations(l, r) for r in xrange(1,len(l)+1)):
            yield list(permutations(subset))

    @staticmethod
    def run(playerList, precision = 4, verbose = False):
        def preciseEnough(list1, list2, precision):
            if type(precision) != int:
                raise TypeError("{0} was of incorrect type. Was {1}, expected {2}", precision.__name__, precision.__class__, int)
            if precision < 0:
                raise ValueError("precision must be non-negative.")
            if len(list1) > 0 and type(list1[0]) != int and type(list1[0]) != long:
                raise TypeError("list1 must be a list of type {0}, not {1}".format(int.__name__, list1[0].__class__.__name__))
            if len(list2) > 0 and type(list2[0]) != int and type(list2[0]) != long:
                raise TypeError("list2 must be a list of type {0}, not {1}".format(int.__name__, list2[0].__class__.__name__))
            if len(list1) != len(list2):
                return False
            if len(list1) == 0:
                return False
            sum1 = sum(list1)
            sum2 = sum(list2)
            formattedList1 = [x/1.0/sum1 for x in list1]
            formattedList2 = [x/1.0/sum2 for x in list2]
            for x in xrange(len(list1)):
                if math.floor(formattedList1[x]*10**precision) != math.floor(formattedList2[x]*10**precision):
                    if verbose:
                        print "Precision at position {0} doesn't match. {1} != {2}".format(x, formattedList1[x], formattedList2[x])
                        print "Precision", precision
                        print "{0} != {1}".format(math.floor(formattedList1[x]*10**precision), math.floor(formattedList2[x]*10**precision))
                        print [x for x in formattedList1]
                        print [x for x in formattedList2]
                    return False
            if verbose:
                print [x for x in formattedList1]
                print [x for x in formattedList2]
            return True
        gameState = GameState(playerList)
        currentRemainingGameStates = [gameState]
        finishedGames = []
        previousSetOfGameSTates = []
        while len(currentRemainingGameStates) > 0 and\
               not preciseEnough([x.occurences for x in currentRemainingGameStates], [x.occurences for x in previousSetOfGameSTates], precision):
            previousSetOfGameSTates = currentRemainingGameStates
            remainingGames = []
            for game in currentRemainingGameStates:
                nightResults = StarWarsPathEvaluator.nightCycle(game)
                finishedGames += nightResults[0]
                remainingGames += nightResults[1]
            currentRemainingGameStates = []
            for game in remainingGames:
                dayResults = StarWarsPathEvaluator.dayCycle(game)
                finishedGames += dayResults[0]
                currentRemainingGameStates += dayResults[1]
            currentRemainingGameStates = reduceStates(currentRemainingGameStates)
            finishedGames = reduceStates(finishedGames)
        return finishedGames

    @staticmethod
    def dayCycle(state):
        '''
            Evaluats possible dayTimeResults
            Returns a list of one of two results:
            1 - List) The game continues with a list of remaining players
            2 - Num) The game has ended

            Possible ways of dying during the day:
              'trial', 'being eaten', 'shot after shooter dies'
        '''
        if state is None:
            raise ValueError( "state was null" )
        if state.evaluateEndConditions() is not None:
            return unzipGameStates(state)

        possibleOutcomes = [state]

        livingActiveEaters = [x for x in swSets.eaters.intersection(state.players) if state.killerStates[x] == 1]
        powerSetPermutationsOfEaters = StarWarsPathEvaluator.powerSetPermutations(livingActiveEaters)
        for eaterSet in powerSetPermutationsOfEaters:
            for eaterPermutation in eaterSet:
                newGameStates = [GameState(otherState = state)]
                for eater in eaterPermutation:
                    currentGameStates = [x for x in newGameStates]
                    for gameState in currentGameStates:
                        if (eater not in gameState.players and eater != gameState.disabledPlayer):
                            newGameStates = [x for x in newGameStates if x != gameState]
                            continue
                        playersWithoutEater = [x for x in gameState.players if x != eater or x in eaterSet and gameState.killerStates[x] != 1 and x not in gameState.playersToDie]
                        for player in playersWithoutEater:
                            newGameState = GameState(otherState = gameState)
                            newGameState.killerStates[eater] = 0
                            newGameState.playersToDie.append(player)
                            newGameStates += handleDeath(newGameState, 0)
                possibleOutcomes += [x for x in newGameStates if x not in possibleOutcomes]

        currentPossibleOutcomes = [x for x in possibleOutcomes]
        possibleOutcomes = []
        for gameState in currentPossibleOutcomes:
            possibleOutcomes += handleDeath(gameState, 0)

        currentPossibleOutcomes = [x for x in possibleOutcomes if not x.isOver]
        for gameState in currentPossibleOutcomes:
            if len(gameState.players) > 2:
                for player in gameState.players:
                    newGameState = GameState(otherState = gameState)
                    newGameState.playersToDie.append(player)
                    possibleOutcomes.append(newGameState)

        currentPossibleOutcomes = [x for x in possibleOutcomes]
        possibleOutcomes = []
        for gameState in currentPossibleOutcomes:
            possibleOutcomes += handleDeath(gameState, 0)

        for gameState in possibleOutcomes:
            gameState.disabledPlayer = None
            if gameState.resurectStorm:
                gameState.players.append('storm')
                gameState.resurectStorm = False
            gameState.evaluateEndConditions()

        return unzipGameStates(reduceStates(possibleOutcomes))

    @staticmethod
    def nightCycle(state):
        '''
            Evaluates possible dayTimeResults
            Returns a list of one of two results:
            1 - List) The game continues with a list of remaining players
            2 - Num) The game has ended

            Possible ways of dying during the night:
              'sith kills', 'shot after shooter dies', 'incineration', 'thermal detinator'
        '''
        if (state.evaluateEndConditions() is not None):
            return unzipGameStates(state)

        possibleOutcomes = []
        protected = None

        #Sith kill
        postSithOutcomes = []
        highestSith = 'emperor' if 'emperor' in state.players else 'darth'
        playersWithoutHighestSith = [x for x in state.players if x != highestSith]
        for player in playersWithoutHighestSith:
            newGameState = GameState(otherState = state)
            newGameState.playersToDie.append(player)
            postSithOutcomes.append(newGameState)
        possibleOutcomes += postSithOutcomes

        if 'yoda' in state.players:
            currentPossibleOutcomes = [x for x in possibleOutcomes]
            possibleOutcomes = []
            outcomesWithProtection = []
            for outcome in currentPossibleOutcomes:            
                for player in [x for x in outcome.players if x != 'yoda']:
                    newGameState = GameState(otherState = outcome)
                    newGameState.protectedPlayer = player
                    outcomesWithProtection.append(newGameState)
            possibleOutcomes += outcomesWithProtection

        if 'luke' in state.players:
            currentPossibleOutcomes = [x for x in possibleOutcomes]
            outcomesWithChallenge = []
            for outcome in currentPossibleOutcomes:
                for player in [x for x in state.players if x != 'luke']:
                    newGameState = GameState(otherState = outcome)
                    newGameState.playersToDie.append(player)
                    if player in swSets.good and player != newGameState.protectedPlayer:
                        newGameState.playersToDie.append('luke')
                    outcomesWithChallenge.append(newGameState)
            possibleOutcomes += outcomesWithChallenge

        if 'bathan' in state.players:
            currentPossibleOutcomes = [x for x in possibleOutcomes]
            outComesWithIncineration = []
            for outcome in currentPossibleOutcomes:
                for player in [x for x in state.players if x != 'bathan']:
                    newGameState = GameState(otherState = outcome)
                    newGameState.playersToDie.append(player)
                    outComesWithIncineration.append(newGameState)
            possibleOutcomes += outComesWithIncineration

        if 'ev' in state.players:
            currentPossibleOutcomes = [x for x in possibleOutcomes]
            outcomesWithDisable = []
            for outcome in currentPossibleOutcomes:
                for player in [x for x in state.players if x != 'ev']:
                    newGameState = GameState(otherState = outcome)
                    newGameState.disabledPlayer = player
                    outcomesWithDisable.append(newGameState)
            possibleOutcomes += outcomesWithDisable

        evaluatedOutcomes = []
        for outcome in possibleOutcomes:
            evaluatedOutcomes += handleDeath(outcome, len(outcome.playersToDie))
        for outcome in evaluatedOutcomes:
            outcome.protectedPlayer = None
            outcome.evaluateEndConditions()
        return unzipGameStates(reduceStates(evaluatedOutcomes))
