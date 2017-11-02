''' what's going on lately in the city? '''
from datetime import datetime
import random
import tracery
from utilities import get_latin, format_text

class News(object):
    ''' newsworthy events for the city '''

    def __init__(self, government, genders, politics, lang):
        self.government = government
        self.lang = lang
        self.genders = genders
        self.politics = politics
        self.surname_first = bool(random.getrandbits(1))

        # the type of government determines who's who
        self.rulers = []
        if government in ['monarchy', 'theocracy']:
            title = 'Emperor'
            self.rulers.append(self.get_person('ruler', title))
        else:
            # oligarchy or republic
            title = 'head of a ruling family'
            for i in range(0, random.randint(3, 7)):
                self.rulers.append(self.get_person('oligarch' + str(i), title))

        self.aristocracy = []
        for i in range(0, random.randint(10, 30)):
            if government in ['monarchy', 'theocracy']:
                title = 'cousin of the Emperor'
            else:
                title = 'cousin to a head of state'
            self.aristocracy.append(
                self.get_person('aristocrat' + str(i), title))


    def generate_event(self, year):
        ''' generate headlines '''
        headlines = []
        # is it time for a change of power?
        if year % self.politics['term_length'] == 0 or \
                random.random() < self.politics['stability']:
            # it's time for a transition of power
            headlines = self.power_shift(year)
        elif year == datetime.now().year:
            # scandals from last year are boring
            headlines = self.scandal()

        return {
            'year': year,
            'headlines': headlines,
        }


    def scandal(self):
        ''' generate a scandal in the upper classes '''
        person = random.choice(self.aristocracy)
        return [person['name'] + ', ' + \
                person['title'] + ', did a scandelous thing']


    def power_shift(self, year):
        ''' the king is dead '''
        ruler_index = random.randint(0, len(self.rulers) - 1)

        deposed = self.rulers[ruler_index]
        replacement = self.get_person('new_ruler' + str(year), deposed['title'])

        self.rulers[ruler_index] = replacement

        if year % self.politics['term_length'] == 0:
            # peaceful/expected shift of power
            if self.politics['term_length'] == 80:
                actions = ['#peaceful_life# and will be succeeded '\
                            'by their #child#, %s' % replacement['name']]
            else:
                actions = ['#peaceful_term# and their position be ' \
                            'taken up by %s' % replacement['name']]
        else:
            actions = ['was deposed in a coupe orchestrated by their #deposer#',
                       'was murdered by their #deposer#']

        rules = {
            'start': 'Ruler %s #action#' % deposed['name'],
            'action': actions,
            'peaceful_life': [
                'died peacefully', 'died in their sleep', 'retired',
                'passed away', 'stepped down after a long rein'],
            'peaceful_term': ['completed their term in office', 'retired'],
            'deposer': '#relationship#, %s' % replacement['name'],
            'relationship': ['#relation#'],
            'relation': [
                '#age# #child#', 'uncle', 'aunt', 'cousin', 'nephew', 'niece'],
            'age': ['youngest', 'second', 'third', 'fifth',
                    'seventh', 'eldest'],
            'child': ['son', 'daughter'] if self.genders == 2 else ['child'],
        }
        grammar = tracery.Grammar(rules)
        sentence = grammar.flatten('#start#')

        headlines = [format_text(sentence)]

        # and a new ruler takes over
        headlines.append('%s is crowned' % replacement['name'])
        return headlines


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
            'gender': random.randint(0, self.genders)
        }


    def get_name(self, given_name, surname):
        ''' just print out the latin name of whoever '''
        name = [get_latin(surname, capitalize=True),
                get_latin(given_name, capitalize=True)]
        return ' '.join(name) if self.surname_first else ' '.join(name[::-1])

