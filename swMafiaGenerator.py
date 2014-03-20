from sets import Set

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

    good = Set(['ewok', 'obi', 'laya', 'han', 'ackbar', 'yoda', 'luke', 'bathan'])
    bad = Set(['bounty', 'storm', 'probe', 'ev'])
    sith = Set(['emperor', 'darth'])

    eaters = Set(['chewbacca', 'rancor'])
    shooters = Set(['han', 'bounty'])
    nightKillers = sith.union(Set(['luke', 'bathan']))

    @staticmethod
    def endConditions(playList):
        '''
            If 'Good' wins: positive
            If 'Bad' wins: negative
            0 for stalemate
            None if the game is still going
        '''
        if (playList == None or len(playList) == 0):
            return 0
        if (len(StarWarsPathEvaluator.sith.intersection(playList)) == 0):
            return len(StarWarsPathEvaluator.good.intersection(playList))
        else:
            if (len(StarWarsPathEvaluator.good.intersection(playList)) == 0):
                return -1
        return None

    @staticmethod
    def dayCycle(playList):
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
        currentGameState = StarWarsPathEvaluator.endConditions(playList)
        if (currentGameState is not None):
            return [currentGameState]

        possibleOutcomes = []
        for player in playList:
            postTrialList = [x for x in playList if x != player]
            if (player not in StarWarsPathEvaluator.shooters):
                possibleOutcomes += [postTrialList]
            else:
                for shotPlayer in postTrialList:
                    possibleOutcomes += [[x for x in postTrialList if x != shotPlayer]]

        print ">>"
        print possibleOutcomes
        print "<<"
        livingEaters = StarWarsPathEvaluator.eaters.intersection(playList)
        for eater in livingEaters:
            playersWithoutEater = [x for x in playList if x != eater]
            for player in playersWithoutEater:
                possibleOutcomes += [[x for x in playList if x != player]]

        return possibleOutcomes
