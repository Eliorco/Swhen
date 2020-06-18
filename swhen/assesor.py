import logging


class Assesor:
    '''
    assess data from API and get a score of the session
    '''
    def __init__(self, data):
        self.score = 0
        self.tests = []
        self.data = data

    def wave_hight_score(self):
        """
        'nice': 0.6 - 0.8,
        'great': 0.9-1.2,
        'storm': 1.3-2,3,4
        """
        weight = {
            'bad': (0.4,9),
            'nice': (1.1,20),
            'great': (2,30),
            'storm': (1, 15),
            'unknown': (3, 90)
        }
        str_result = 'unknown'
        result = 0
        if (self.data['swell']['absMinBreakingHeight'] >= 0.5 and self.data['swell'][
            'absMaxBreakingHeight'] < 0.9):
            str_result = 'nice'
        elif (self.data['swell']['absMinBreakingHeight'] > 0.89 and self.data['swell'][
            'absMaxBreakingHeight'] < 1.2):
            str_result = 'great'
        elif (self.data['swell']['absMinBreakingHeight'] > 1.3 and self.data['swell'][
            'absMaxBreakingHeight'] < 4):
            str_result = 'storm'
        elif (self.data['swell']['absMinBreakingHeight'] < 0.5 and self.data['swell'][
            'absMaxBreakingHeight'] < 0.6):
            str_result = 'bad'

        result = weight[str_result][0] * weight[str_result][1]
        print(f"assess score is {str_result}: ", result)
        return result

    @staticmethod
    def surf_conditions_score():
        # TODO: implement it soon
        return 0

    def assess_session(self):
        """
        swell score: 60%
        conditions: 40%
        :return:
        """
        return self.wave_hight_score()*0.6 + self.surf_conditions_score()*0.4
