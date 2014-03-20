from starWarsMafiaGameState import StarWarsMafiaGameState as GameState
from starWarsMafiaGameState import StarWarsSets as swSets

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


        TODO keep way of tracking eaters and bothan state
        TODO track EV
    '''

    @staticmethod
    def dayCycle(state):
        '''
            Evaluats possible dayTimeResults
            Returns a list of one of two results:
            1 - List) The game continues with a list of remaining players
            2 - Num) The game has ended

            Possible ways of dying during the day:
              'trial', 'being eaten', 'shot after shooter dies'

            TODO:
                Shooters
                EV
        '''
        currentGameState = state.evaluateEndConditions()
        if (currentGameState is not None):
            return [state]

        possibleOutcomes = [state.players]
        for player in state.players:
            postTrialList = [x for x in state.players if x != player]
            if (player not in swSets.shooters):
                possibleOutcomes += [postTrialList]
            else:
                for shotPlayer in postTrialList:
                    possibleOutcomes += [[x for x in postTrialList if x != shotPlayer]]

        print ">>"
        print possibleOutcomes
        print "<<"
        livingEaters = swSets.eaters.intersection(state.players)
        for eater in livingEaters:
            playersWithoutEater = [x for x in state.players if x != eater]
            for player in playersWithoutEater:
                possibleOutcomes += [[x for x in state.players if x != player]]

        return possibleOutcomes
