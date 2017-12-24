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
        self.data['isolation'] = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5])
        # how culturally conservative it is
        self.data['insularity'] = random.randint(self.data['isolation'], 5)
        # isolation means lower max population
        self.data['population'] = random.randint(
            1000 * self.data['isolation'],
            int(10000000/(self.data['isolation'] ** 4))
        )
        self.data['minorities'] = 0

        self.date = datetime.strptime(
            str(datetime.now().year - self.data['city_age']), '%Y')

        self.stability = random.randint(90, 100) / 100.0
        self.economy = random.randint(5, 10) / 10.0
        self.term = 0
        self.ruler = None

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
        while self.date < datetime.now():
            action = None
            # construct something new maybe
            if random.random() > self.economy:
                building = random.choice(self.data['building'])
                buildings[building].append(
                    self.get_building(building))

            # results of an unstable situation
            if self.ruler['duration'] > 7 and \
                    random.random() > self.stability:
                action = random.choice(events['instability']['result'])

            elif self.ruler['duration'] >= self.term:
                # peaceful, expected transition of power
                self.powershift(violent=False)
                self.stability += self.stability * 0.15

            if self.date.month == 1 and self.date.day == 1:
                # events that can occur once per year
                if random.random() > (self.data['insularity'] * 2) / 10.0:
                    action = 'immigration'

            if action and events[action]['generator']:
                events[action]['generator']()

            self.date += timedelta(days=1)
            self.stability += self.stability * 0.5
            self.ruler['duration'] += 1

        self.data['history'] = self.history
        self.data['holidays'] = holidays
        self.data['buildings'] = buildings
        return self.data


    def powershift(self, violent=True):
        ''' the king is dead long live the king '''
        is_republic = self.data['government'] == 'republic'

        if self.ruler:
            if violent:
                end_text = 'Overthrow of %s' % self.ruler['name']
            elif is_republic:
                end_text = 'End of term for %s' % self.ruler['name']
            else:
                end_text = 'Death of %s' % self.ruler['name']

            self.history[self.pretty_date()].append(end_text)

        self.ruler = self.get_person(
            'ruler' + self.pretty_date(),
            'Emperor'
        )

        corronation_date = self.date + timedelta(
            days=random.normalvariate(5, 2))
        coronation = 'Election' if is_republic else 'Coronation'
        self.history[self.pretty_date(corronation_date)].append(
            '%s of %s' % (coronation, self.ruler['name'])
        )

        self.term = (random.randint(2, 10) \
            if is_republic else random.normalvariate(60, 10)) * 365


    def instability(self):
        ''' undermine the government '''
        self.stability = random.randint(0, 70) / 100.0


    def immigration(self):
        ''' a flood of newcomers trying to find a better life '''
        self.stability -= self.stability * 0.05
        self.data['population'] += random.normalvariate(
            (self.data['population']/10), 200)

        self.data['minorities'] += 1
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
        return self.date.strftime(formatter)

