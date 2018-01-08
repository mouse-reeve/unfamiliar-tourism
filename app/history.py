''' the events in the city's history '''
from collections import defaultdict
from datetime import datetime, timedelta
import random
from utilities import get_latin

class History(object):
    ''' generate history '''

    def __init__(self, data, lang):
        self.data = data
        self.lang = lang
        self.lang.surname_first = bool(random.getrandbits(1))

        # ----- Starting stats
        self.data['city_age'] = random.choice([50] + [500] * 5 + [1000] * 10)

        # physical isolation / remoteness
        isolation = random.randint(4, 10) / 10.0

        self.status = {
            'date': datetime.strptime(
                str(datetime.now().year - self.data['city_age']), '%Y'),
            'stability': random.randint(90, 100) / 100.0,
            'isolation': isolation,
            'insularity': random.randint(int(isolation * 10), 10) / 10.0,
            'population': random.randint(
                1000 * isolation, int(10000000/(isolation ** 4))),
            'minorities': 0,
            'economy': random.randint(5, 10) / 10.0,
            'term': 0,
            'ruler': None
        }
        print(self.status)

        self.history = defaultdict(lambda: [])

    def generate_history(self):
        ''' fill out time '''
        events = {
            'invasion': {
                'result': ['powershift', 'dieout'],
                'generator': None
            },
            'dieout': {
                'result': ['instability', None],
                'generator': None
            },
            'powershift': {
                'result': ['innovation', 'classicism', 'modernism',
                           'instability', None],
                'generator': self.powershift
            },
            'innovation': {
                'result': ['bumpercrop', 'bumpercrop', 'disaster'],
                'generator': None
            },
            'disaster': {
                'result': ['powershift', None],
                'generator': None
            },
            'bumpercrop': {
                'result': ['innovation', None],
                'generator': None
            },
            'classicism': {
                'result': [],
                'generator': None
            },
            'modernism': {
                'result': [],
                'generator': None
            },
            'immigration': {
                'result': ['bumpercrop', None],
                'generator': self.immigration
            },
            'revolution': {
                'result': ['powershift', 'dieout'],
                'generator': None
            },
            'instability': {
                'result': ['powershift', 'revolution', 'religiosity'],
                'generator': self.instability
            },
            'religiosity': {
                'result': ['instability', 'classicism', None],
                'generator': None
            },
        }


        buildings = {b: [] for b in self.data['building']}
        holidays = []

        self.history[self.pretty_date()] = ['The city was founded']

        self.powershift(violent=False)
        while self.status['date'] < datetime.now():
            action = None
            # construct something new maybe
            if random.random() > self.status['economy']:
                building = random.choice(self.data['building'])
                buildings[building].append(
                    self.get_building(building))

            # results of an unstable situation
            if self.status['ruler']['duration'] > 7 and \
                    random.random() > self.status['stability']:
                action = random.choice(events['instability']['result'])

            elif self.status['ruler']['duration'] >= self.status['term']:
                # peaceful, expected transition of power
                self.powershift(violent=False)
                self.status['stability'] += self.status['stability'] * 0.15

            # events that can occur once per year
            if self.status['date'].month == 1 and self.status['date'].day == 1:
                if self.status['date'].year + 50 > datetime.now().year and \
                        self.status['date'].year % 10 == 0 and \
                        random.random() > self.status['insularity'] * 2:
                    action = 'immigration'

            if action and events[action]['generator']:
                events[action]['generator']()

            self.status['date'] += timedelta(days=1)
            self.status['stability'] += self.status['stability'] * 0.5
            self.status['ruler']['duration'] += 1

        self.data['history'] = self.history
        self.data['holidays'] = holidays
        self.data['buildings'] = buildings

        self.status['date'] = self.status['date'].isoformat()
        self.data['status'] = self.status
        return self.data


    def powershift(self, violent=True):
        ''' the king is dead long live the king '''
        is_republic = self.data['government'] == 'republic'

        if self.status['ruler']:
            if violent:
                end_text = 'Overthrow of %s' % self.status['ruler']['name']
            elif is_republic:
                end_text = 'End of term for %s' % self.status['ruler']['name']
            else:
                end_text = 'Death of %s' % self.status['ruler']['name']

            self.history[self.pretty_date()].append(end_text)

        self.status['ruler'] = self.get_person(
            'ruler' + self.pretty_date(),
            'Emperor'
        )

        corronation_date = self.status['date'] + timedelta(
            days=int(random.normalvariate(5, 2)))
        coronation = 'Election' if is_republic else 'Coronation'
        self.history[self.pretty_date(corronation_date)].append(
            '%s of %s' % (coronation, self.status['ruler']['name'])
        )

        self.status['term'] = (random.randint(2, 10) \
            if is_republic else int(random.normalvariate(50, 10))) * 365


    def instability(self):
        ''' undermine the government '''
        self.status['stability'] = random.randint(0, 70) / 100.0


    def immigration(self):
        ''' a flood of newcomers trying to find a better life '''
        self.status['stability'] -= self.status['stability'] * 0.05

        self.status['minorities'] += 1
        self.history[self.pretty_date()].append('A flood of immigrants')


    def get_person(self, identifier, title, surname=None):
        ''' create a basic person bio '''
        given_name = self.lang.get_word('NNP', identifier+'given')
        surname = surname or self.lang.get_word('NNP', identifier+'sur')
        fullname = self.get_name(given_name, surname)
        return {
            'given_name': given_name,
            'surname': surname,
            'name': fullname,
            'title': title,
            'gender': random.randint(0, len(self.data['genders'])),
            'duration': 0
        }


    def get_name(self, given_name, surname):
        ''' just print out the latin name of whoever '''
        name = [get_latin(surname, capitalize=True),
                get_latin(given_name, capitalize=True)]
        return ' '.join(name) if self.lang.surname_first else \
               ' '.join(name[::-1])


    def get_building(self, building):
        ''' info on a building '''
        return {
            'built': self.pretty_date(),
            'type': building,
        }


    def pretty_date(self, date=None):
        ''' format dates '''
        formatter = '%Y-%m-%d'
        if date:
            return date.strftime(formatter)
        return self.status['date'].strftime(formatter)

